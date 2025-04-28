import os
from dotenv import load_dotenv
import asyncio
from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.pdfmetrics import stringWidth

# 載入 .env 檔案中的環境變數
load_dotenv()

log_output = []

def generate_pdf(log):
    print("正在輸出pdf請稍後...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"食材管理機器人對話紀錄_{timestamp}.pdf"

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

    text_object = c.beginText(50, height - 50)
    text_object.setFont('STSong-Light', 12)
    line_spacing = 18
    max_width = 480

    ai_mode = False  # ⚡ 這個變數：記錄現在是不是在寫 AI 回應

    for entry in log:
        clean_entry = entry.replace("�", "").strip()
        lines = clean_entry.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 遇到 "你輸入了" 就正常寫在原本頁面
            if line.startswith("你輸入了："):
                if ai_mode:
                    # 如果前面是 AI 回應，結束那頁，開新頁
                    c.drawText(text_object)
                    c.showPage()
                    text_object = c.beginText(50, height - 50)
                    text_object.setFont('STSong-Light', 12)
                    ai_mode = False

                if text_object.getY() <= 70:
                    c.drawText(text_object)
                    c.showPage()
                    text_object = c.beginText(50, height - 50)
                    text_object.setFont('STSong-Light', 12)

                text_object.setFont('STSong-Light', 14)
                text_object.textLine(line)
                text_object.moveCursor(0, line_spacing)
                text_object.setFont('STSong-Light', 12)

            # 遇到 "AI 回應：" 要換新的一整頁來寫
            elif line.startswith("AI 回應："):
                # 如果現在還沒在 AI 回應模式，換頁開始寫
                if not ai_mode:
                    c.drawText(text_object)
                    c.showPage()
                    text_object = c.beginText(50, height - 50)
                    text_object.setFont('STSong-Light', 14)
                    text_object.textLine("AI 回應：")
                    text_object.moveCursor(0, line_spacing)
                    text_object.setFont('STSong-Light', 12)
                    ai_mode = True

            else:
                # 正文自動換行處理
                while line:
                    if text_object.getY() <= 70:
                        c.drawText(text_object)
                        c.showPage()
                        text_object = c.beginText(50, height - 50)
                        text_object.setFont('STSong-Light', 12)

                    cut = len(line)
                    while stringWidth(line[:cut], 'STSong-Light', 12) > max_width and cut > 0:
                        cut -= 1
                    text_object.textLine(line[:cut])
                    line = line[cut:]

    # 最後一頁記得畫出來
    c.drawText(text_object)
    c.save()
    print(f"✅ PDF 完整路徑：{os.path.abspath(filename)}")


async def main():

    # 從環境變數中讀取金鑰
    api_key = os.environ.get("GEMINI_API_KEY")

    # 初始化 ChatSession 並選擇模型
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.0-flash",
        api_key=api_key,
    )
    ingredients_list = []

    while True:
        print("歡迎來到食材管理機器人! 請輸入一個食材或輸入 '退出' 結束")
        print("輸入'退出'才會產出pdf檔")

        user_input = input("食材：").strip()

        if user_input.lower() == "退出":
            print("感謝使用!")
            break
        
        ingredients_list.append(user_input)
        ingredient_number = len(ingredients_list)  # 使用當前列表的長度作為編號
        print(f"輸入的食材編號是: input{ingredient_number} -> {user_input}")
        log_output.append(f"你輸入了：{user_input}")
        
        model_choice = None  # 初始化變數
        
        while model_choice not in ["1", "2"]:
            model_choice = input("請選擇模型:\n1. 食譜建議模型\n2. 食材保存建議模型\n請輸入 1 或 2：").strip()
            
            if model_choice == "1":
                print("是否需要繼續輸入食材")
                user_check = input("(Yes/No)：").strip()

                while user_check.lower() == "yes":
                    print("請輸入食材")
                    user_input = input("食材：").strip()

                    # 加入食材到列表
                    ingredients_list.append(user_input)
                    ingredient_number = len(ingredients_list)  # 使用當前列表的長度作為編號
                    print(f"輸入的食材編號是: input{ingredient_number} -> {user_input}")
                    log_output.append(f"你輸入了：{user_input}")

                    # 繼續詢問是否需要輸入更多食材
                    print("是否需要繼續輸入食材")
                    user_check = input("(Yes/No)：").strip()
                    if user_check =="No":
                        break

                print("請輸入烹飪方式(例如：煎、炒、烘、煮、炸、甜點)")
                user_cook1 = input("請輸入烹飪方式:").strip()
                print("請輸入飲食目標(例如：低卡路里、高蛋白、素食、減醣、增肌、無特殊要求、改善心血管健康)")
                user_cook2 = input("請輸入飲食目標:").strip()
                # 當所有食材輸入完成後，向 AI 發送請求
                response = await model_client.create([UserMessage(content=f"根據這些食材給我一些食譜建議：{', '.join(ingredients_list)}，並考慮烹飪方式{user_cook1} 和 飲食目標{user_cook2}。", source="user")])
                print("AI 回應:", response.content)
                log_output.append(f"AI 回應：{response.content}")
                ingredients_list.clear()
                break

            elif model_choice == "2":
                    response = await model_client.create([UserMessage(content=f"給予正確的保存建議{ingredients_list}", source="user")])
                    print("AI 回應:", response.content)
                    log_output.append(f"AI 回應：{response.content}")
                    ingredients_list.clear()
                    break
            else:
                print("輸入錯誤，請重新輸入 1 或 2。")
                model_choice = None
    generate_pdf(log_output)
                

if __name__ == '__main__':
    asyncio.run(main())