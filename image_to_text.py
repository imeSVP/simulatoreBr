from paddleocr import PaddleOCR


# 全局初始化，只加载一次
ocr = PaddleOCR(
    lang="it",
    use_angle_cls=False
)


def image_to_text(image_path):
    """
    图片转文字
    """

    result = ocr.ocr(
        image_path,
        cls=False
    )

    texts = []

    for page in result:
        if page:
            for line in page:
                text = line[1][0]
                texts.append(text)

    return "\n".join(texts)



if __name__ == "__main__":

    text = image_to_text(
        "image_0.png"
    )

    print(text)
