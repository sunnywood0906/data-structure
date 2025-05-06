import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template_string, redirect, url_for, send_file
import asyncio
from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.pdfmetrics import stringWidth

# 載入 .env 檔案中的環境變數
load_dotenv()

app = Flask(__name__)
conversation_log = []
# 初始化模型用戶端
api_key = os.environ.get("GEMINI_API_KEY")
model_client = OpenAIChatCompletionClient(
    model="gemini-2.0-flash",
    api_key=api_key,
)

ingredients_list = []
latest_response = None

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>食材管理機器人</title>
    <style>
        body {
            font-family: "Segoe UI", "Microsoft JhengHei", sans-serif;
            background-color: #ffffff;
            max-width: 800px;
            margin: auto;
            padding: 2em;
            color: #2c3e50;
        }
        h1 {
            text-align: center;
            font-size: 2.8em;
            margin-bottom: 1em;
        }
        h2, h3 {
            margin-top: 1.5em;
        }
        form {
            margin-bottom: 1.5em;
            background-color: #fff0f5;
            padding: 1.5em;
            border-radius: 16px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.06);
        }
        input[type="text"], select {
            width: calc(100% - 140px);
            padding: 0.7em;
            margin-bottom: 0.5em;
            border: 2px solid #f3c1d3;
            border-radius: 10px;
            font-size: 1em;
        }
        .hidden-input {
            display: none;
            margin-top: 0.5em;
        }
        button {
            padding: 0.7em 1.4em;
            background-color: #f7a1c4;
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-size: 1em;
            transition: 0.3s ease;
        }
        button:hover {
            background-color: #e989b3;
        }
        .ingredient-list {
            background-color: #fff8fb;
            padding: 1em;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            font-size: 1.05em;
        }
        .ingredient-item {
            margin-bottom: 0.4em;
        }
        .response-box {
            background-color: #fff5fa;
            padding: 1em 1.5em;
            border-left: 6px solid #f7a1c4;
            border-radius: 12px;
            margin-top: 1em;
            font-size: 1.1em;
            white-space: pre-wrap;
            line-height: 1.7em;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        .response-box h3 {
            margin-top: 0;
            margin-bottom: 0.5em;
        }
    </style>
    <script>
        function toggleOtherInput(selectElem, inputId) {
            var inputElem = document.getElementById(inputId);
            if (selectElem.value === '其他') {
                inputElem.style.display = 'block';
            } else {
                inputElem.style.display = 'none';
                inputElem.value = '';
            }
        }
    </script>
</head>
<body>
    <h1>食材管理機器人</h1>

    <h2>輸入食材</h2>
    <form action="/input" method="post">
        <input type="text" name="ingredient" placeholder="請輸入食材">
        <button type="submit">新增</button>
    </form>
    <form action="/reset" method="post" style="display: inline-block;">
        <button type="submit">重設食材清單</button>
    </form>
    <form action="/delete_last" method="post" style="display: inline-block;">
        <button type="submit">刪除最後一項</button>
    </form>

    <h3>目前已輸入的食材：</h3>
    <div class="ingredient-list">
        {% for item in ingredients %}
            <div class="ingredient-item">{{ loop.index }} {{ item }}</div>
        {% else %}
            <div class="ingredient-item">（尚未輸入任何食材）</div>
        {% endfor %}
    </div>

    <h2>食譜建議</h2>
    <form action="/suggest/recipe" method="post">
        <label>選擇烹飪方式：</label><br>
        <select name="cook_method" onchange="toggleOtherInput(this, 'cook_other')">
            <option value="煎">煎</option>
            <option value="炒">炒</option>
            <option value="烘">烘</option>
            <option value="煮">煮</option>
            <option value="炸">炸</option>
            <option value="甜點">甜點</option>
            <option value="其他">其他</option>
        </select>
        <input type="text" id="cook_other" name="cook_other" placeholder="請輸入其他烹飪方式" class="hidden-input"><br><br>

        <label>選擇飲食目標：</label><br>
        <select name="diet_goal" onchange="toggleOtherInput(this, 'diet_other')">
            <option value="低卡路里">低卡路里</option>
            <option value="高蛋白">高蛋白</option>
            <option value="素食">素食</option>
            <option value="減醣">減醣</option>
            <option value="增肌">增肌</option>
            <option value="無特殊要求">無特殊要求</option>
            <option value="改善心血管健康">改善心血管健康</option>
            <option value="其他">其他</option>
        </select>
        <input type="text" id="diet_other" name="diet_other" placeholder="請輸入其他飲食目標" class="hidden-input"><br><br>

        <button type="submit">取得食譜建議</button>
    </form>

    <h2>保存建議</h2>
    <form action="/suggest/storage" method="post">
        <button type="submit">取得保存建議</button>
    </form>

    {% if message %}
        <div class="response-box">
            <h3>AI 回應：</h3>
            <p>{{ message }}</p>
            <form action="/download" method="post">
                <button type="submit">下載為 PDF</button>
            </form>
        </div>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_FORM, ingredients=ingredients_list, message=latest_response)

@app.route('/suggest/recipe', methods=['POST'])
def suggest_recipe():
    global latest_response

    async def run_prompt():
        cook_method = request.form.get("cook_method", "")
        cook_other = request.form.get("cook_other", "").strip()
        if cook_method == "其他" and cook_other:
            cook_method = cook_other

        diet_goal = request.form.get("diet_goal", "")
        diet_other = request.form.get("diet_other", "").strip()
        if diet_goal == "其他" and diet_other:
            diet_goal = diet_other

        if not ingredients_list:
            return "目前沒有任何食材，請先輸入食材"

        prompt_message = (
            f"下列是使用者輸入的條件：\n"
            f"食材：{', '.join(ingredients_list)}\n"
            f"烹飪方式：{cook_method}\n"
            f"飲食目標：{diet_goal}\n\n"
            f"請根據這些條件給出 1-2 道料理建議，清楚列出料理名稱、所需食材、作法與簡單的營養說明。"
        )

        response = await model_client.create([UserMessage(content=prompt_message, source="user")])
        conversation_log.append(f"你輸入了：{prompt_message}")
        conversation_log.append(f"AI 回應：\n{response.content}")
        return response.content

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    latest_response = loop.run_until_complete(run_prompt())
    return render_template_string(HTML_FORM, message=latest_response, ingredients=ingredients_list)

@app.route('/suggest/storage', methods=['POST'])
def suggest_storage():
    global latest_response

    async def run_storage():
        if not ingredients_list:
            return "目前沒有任何食材，請先輸入食材"

        prompt_message = (
            f"請針對以下食材提供適當的保存建議：{', '.join(ingredients_list)}。"
            f"請將每種食材的建議分點列出，包含：保存方法、建議溫度、保存期限與避免事項。"
        )

        response = await model_client.create([UserMessage(content=prompt_message, source="user")])
        return response.content

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    latest_response = loop.run_until_complete(run_prompt())
    conversation_log.append(f"你輸入了：{prompt_message}")
    conversation_log.append(f"AI 回應：\n{latest_response}")
    return render_template_string(HTML_FORM, message=latest_response, ingredients=ingredients_list)

@app.route('/download', methods=['POST'])
def download_pdf():
    if not conversation_log:
        return redirect(url_for('index'))

    buffer = BytesIO()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"食材管理機器人對話紀錄_{timestamp}.pdf"

    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

    text_object = c.beginText(50, height - 50)
    text_object.setFont('STSong-Light', 12)
    line_spacing = 18
    max_width = 480

    ai_mode = False

    for entry in conversation_log:
        clean_entry = entry.replace("�", "").strip()
        lines = clean_entry.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("你輸入了："):
                if ai_mode:
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

            elif line.startswith("AI 回應："):
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

    c.drawText(text_object)
    c.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

@app.route('/input', methods=['POST'])
def add_ingredient():
    ingredient = request.form.get("ingredient", "").strip()
    if ingredient:
        ingredients_list.append(ingredient)
        ingredient_number = len(ingredients_list)
        return render_template_string(HTML_FORM, message=f"輸入的食材編號是: input{ingredient_number} -> {ingredient}", ingredients=ingredients_list)
    return render_template_string(HTML_FORM, message="請輸入食材", ingredients=ingredients_list)

@app.route('/reset', methods=['POST'])
def reset_ingredients():
    ingredients_list.clear()
    return render_template_string(HTML_FORM, message="食材清單已重設", ingredients=ingredients_list)

@app.route('/delete_last', methods=['POST'])
def delete_last():
    if ingredients_list:
        removed = ingredients_list.pop()
        return render_template_string(HTML_FORM, message=f"已刪除最後一項：{removed}", ingredients=ingredients_list)
    return render_template_string(HTML_FORM, message="目前沒有食材可刪除", ingredients=ingredients_list)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)