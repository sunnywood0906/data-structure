<h3>歡迎來到我的Github :tada::tada:
<P><h2>【以下是我的資料結構課程作業】</P>
<p><h3>HW1-食材管理機器人</p>
<ul style='list-style-type'>
     <li><h4>名稱：食材管理機器人</h4></li>
     <li><h4>功能介紹：
       <ul style='list-style-type'>
       <li><h5>1.可選擇食譜建議模型和食材保存建議模型。</h5></li>
       <li><h5>2.可輸入多項食材給予食譜建議。</h5></li>
       <li><h5>3.可自由輸入偏好烹飪方式和飲食目標讓Ai根據您的喜好設計食譜。</h5></li>
       <li><h5>4.選擇食材保存建議模型Ai即可給予詳細食材保存建議</h5></li>
       </ul>    
     </h4></li>
     <li><h4>流程圖：</h4></li>
     <img src="https://raw.githubusercontent.com/sunnywood0906/data-structure/main/recipe_suggester.png" alt="Recipe Suggester" width="500">
     <li><h4>主要程式碼：</h4></li>
          https://github.com/sunnywood0906/data-structure/blob/main/recipe_suggester.py
      <li><h4>介紹影片：</h4></li>
          (有聲播放 :loud_sound:)https://youtu.be/9vcjv4ZhzGY
     
</ul>
<p><h3>HW2-諮商分析機器人</p>
<ul style='list-style-type'>
     <li><h4>名稱：諮商分析機器人</h4></li>
     <li><h4>功能介紹：
       <ul style='list-style-type'>
       <li><h5>1.根據心理諮商個案的對話以各項指標判斷個案面臨的問題。</h5></li>
       <li><h5>2.多方位的指標判斷更能貼近個案實際心理狀況。</h5></li>
       <li><h5>3.由AI判斷節省人力審查時間。</h5></li>
       <li><h5>4.指標判斷輸出CSV檔一覽無遺。</h5></li>
       <li><h5>※範例僅由AI生成，無引用特定人之話語！範例資訊：https://github.com/sunnywood0906/data-structure/blob/main/data_analysis.csv</h5></li>
       <li><h5>※指標判斷輸出範例：https://github.com/sunnywood0906/data-structure/blob/main/113_batch.csv</h5></li>
       </ul>    
     </h4></li>
     <li><h4>主要程式碼：</h4></li>
          https://github.com/sunnywood0906/data-structure/blob/main/analysis.py
</ul>
<p><h3>HW3-playwright應用</p>
<ul style='list-style-type'>
     <li><h4>名稱：playwright應用</h4></li>
     <li><h4>功能介紹：
       <ul style='list-style-type'>
       <li><h5>1.此項僅展示playwright技巧。</h5></li>
       </ul>
       <li><h6>note:我原本想要連結到line noify做每日股價提醒，但考量到我想讓這個功能更加實用，與chatgpt討論後決定改為直接抓取api的方式。</h6></li>
       <ul style='list-style-type'>
       <li><h6>1.playwright需要開啟網頁抓取資料，對於多人使用或是查詢多支股票會耗時較久也會很耗資源。</h6></li>
       <li><h6>2.使用api的話就是直接抓資料很快速也不用像playweright一樣還要下載瀏覽器，比較適合大量查詢和多人使用。</h6></li>
       <li><h6>為了繼續開發所以我沒有直接把要查詢的股票代碼直接打在一起，為了方便助教批閱這邊附上執行結果。</h6></li>
        <img src="https://github.com/sunnywood0906/data-structure/blob/main/%E8%9E%A2%E5%B9%95%E6%93%B7%E5%8F%96%E7%95%AB%E9%9D%A2%202025-04-11%20180345.png" alt="Recipe Suggester" width="500">    
       <li><h6>題外話：會想做這個是因為我每次都忘記看股票都是我媽叫我看，所以想做一個他會直接提醒我的。用playwright自己提醒當然也可以，但我也想給我媽用(很好笑)，而且既然都要做了那當然就直接做好，所以我果斷放棄playwright(抱歉助教我這個作業很廢)，我是真的有經過思考過程的，畢竟做程式就是要應用生活為了交作業而寫真的浪費時間，所以我會花很多時間在完成一項作業因為我每一項幾乎都是為我自己做的(其實作業2原本是要寫分析吵架機器人，可以匯入line文字檔判斷的那種(扯遠了)喔對了這個題外話只是補充我不是想要敷衍作業的題外話我沒有要情勒助教給我好分數)總之我會好好完成的(我連Line Messaging API都拿了)祝大家發大財。</h6></li>
       </ul>  
     </h4></li>
     <li><h4>主要程式碼：</h4></li>
          https://github.com/sunnywood0906/data-structure/blob/main/stock_tracker.py
</ul>

<p><h3>HW4-進階食材管理機器人</p>
<ul style='list-style-type'>
     <li><h4>名稱：進階食材管理機器人</h4></li>
     <li><h4>功能介紹：
       <ul style='list-style-type'>
       <li><h5>1.根據HW1改製成輸出PDF檔的真正食譜機器人。</h5></li>
       <li><h5>2.將AI回覆優化成可自動換行，更容易閱讀。</h5></li>
       <li><h5>3.AI回覆自動跳頁，不怕輸入超多食材。</h5></li>
       <li><h5>4.更早偵測換頁避免因為快速大量輸出而導致換頁吃字。</h5></li>
       <li><h5>5.依據日期及時間命名檔名，不覆蓋下載紀錄。</h5></li>
       <li><h5>6.可一次操作多種食譜及模型最後再一次下載成PDF。</h5></li>
       </ul>    
     </h4></li>
     <li><h4>主要程式碼：</h4></li>
          https://github.com/sunnywood0906/data-structure/blob/main/pdf.py
     <li><h4>範例輸出食譜：</h4></li>
          https://github.com/sunnywood0906/data-structure/blob/main/%E9%A3%9F%E6%9D%90%E7%AE%A1%E7%90%86%E6%A9%9F%E5%99%A8%E4%BA%BA%E5%B0%8D%E8%A9%B1%E7%B4%80%E9%8C%84_20250428_1218.pdf
</ul>

<p><h3>HW5-食材管理機器人網站(含使用介面)</p>
<ul style='list-style-type'>
     <li><h4>名稱：食材管理機器人網站</h4></li>
     <li><h4>功能介紹：
       <ul style='list-style-type'>
       <li><h5>1.根據HW1改製成可以直接在網頁上互動的食材機器人。</h5></li>
       <li><h5>2.結合HW3可以直接在網頁上下載成PDF。</h5></li>
       <li><h5>3.簡潔好看的網頁畫面不怕不會用。</h5></li>
       </ul>    
     </h4></li>
     <li><h4>主要程式碼：</h4></li>
          https://github.com/sunnywood0906/data-structure/blob/main/app.py
     <li><h4>網頁連結：</h4></li>
      <li><h6>note:已透過render上傳供大家測試，requirements也有改一份適合render的版本。</h6></li>
         https://data-structure.onrender.com

