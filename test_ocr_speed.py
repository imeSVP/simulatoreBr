
import os
import time

# 保持笔记本原来的配置
os.environ["FLAGS_use_mkldnn"] = "0"

from paddleocr import PaddleOCR

print("正在初始化 PaddleOCR...")

start_init = time.perf_counter()

ocr = PaddleOCR(
    lang="it",
    use_angle_cls=False,
    use_gpu=False
)

init_time = time.perf_counter() - start_init
print(f"初始化耗时: {init_time:.2f} 秒")


def image_to_text(image_path):
    result = ocr.ocr(image_path, cls=False)

    texts = []

    for page in result:
        if page:
            for line in page:
                texts.append(line[1][0])

    return "\n".join(texts)


if __name__ == "__main__":
    image_path = "image_0.png"

    # 预热，不计入正式测试
    print("\n第一次预热...")
    image_to_text(image_path)

    # 正式测试三次
    times = []

    for i in range(3):
        start = time.perf_counter()
        text = image_to_text(image_path)
        elapsed = time.perf_counter() - start

        times.append(elapsed)
        print(f"第 {i + 1} 次 OCR: {elapsed:.2f} 秒")

    print(f"\n平均耗时: {sum(times) / len(times):.2f} 秒")
    print("\n识别结果：")
    print(text)
