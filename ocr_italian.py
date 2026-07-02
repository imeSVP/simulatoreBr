"""
OCR 意大利语识别 - LightOnOCR-2-1B 版本
"""

import torch
from transformers import LightOnOcrForConditionalGeneration, LightOnOcrProcessor
from PIL import Image
import os

# 检查硬件
if torch.cuda.is_available():
    device = "cuda"
    dtype = torch.bfloat16
    print(f"✅ 使用 GPU: {torch.cuda.get_device_name(0)}")
elif torch.backends.mps.is_available():
    device = "mps"
    dtype = torch.float32
    print("✅ 使用 Apple M 系列芯片 (MPS)")
else:
    device = "cpu"
    dtype = torch.float32
    print("⚠️ 使用 CPU (可能会慢一些)")

# 加载模型（首次运行会自动下载约 1.9GB）
print("📥 正在加载 LightOnOCR 模型，首次运行会下载文件...")
model = LightOnOcrForConditionalGeneration.from_pretrained(
    "lightonai/LightOnOCR-2-1B",
    torch_dtype=dtype
).to(device)

processor = LightOnOcrProcessor.from_pretrained("lightonai/LightOnOCR-2-1B")
print("✅ 模型加载完成！")


def recognize(image_path):
    """
    识别图片中的文字
    
    Args:
        image_path: 图片路径
        
    Returns:
        str: 识别的文字
    """
    try:
        # 打开图片
        image = Image.open(image_path).convert('RGB')
        
        # 构建对话格式
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image}
                ]
            }
        ]
        
        # 处理输入
        inputs = processor.apply_chat_template(
            conversation,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        )
        
        # 移动到设备
        inputs = {
            k: v.to(device=device, dtype=dtype) if v.is_floating_point() else v.to(device) 
            for k, v in inputs.items()
        }
        
        # 生成识别结果
        output_ids = model.generate(**inputs, max_new_tokens=1024)
        
        # 解码
        generated_ids = output_ids[0, inputs["input_ids"].shape[1]:]
        output_text = processor.decode(generated_ids, skip_special_tokens=True)
        
        return output_text.strip()
        
    except Exception as e:
        print(f"❌ 识别失败: {e}")
        return ''


if __name__ == '__main__':
    import sys
    import time
    
    if len(sys.argv) < 2:
        print("用法: python ocr_italian.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    print(f"\n📄 识别图片: {image_path}")
    print("-" * 40)
    
    start = time.time()
    text = recognize(image_path)
    elapsed = time.time() - start
    
    if text:
        print(f"✅ 识别结果:\n{text}")
    else:
        print("❌ 未识别到文字")
    
    print(f"⏱️ 耗时: {elapsed:.2f}秒")
