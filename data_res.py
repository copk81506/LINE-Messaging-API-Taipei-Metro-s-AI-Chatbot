def query(query):

    import faiss
    from transformers import AutoTokenizer,RobertaForSequenceClassification
    from transformers import pipeline
    import numpy as np
    from langchain.embeddings import HuggingFaceEmbeddings

    # 載入embedding方式
    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-large-zh-v1.5",
        # model_kwargs={"device": "cuda:0"},  # 若使用 GPU可開啟 
        encode_kwargs={"normalize_embeddings": True}
)

    # 讀取 FAISS 索引，路徑寫.faiss檔案的路徑
    index = faiss.read_index("your-.faiss-path")

    # 使用者查詢及指定分類

    # 載入訓練後的模型，路徑為nlp_model檔案的資料夾路徑
    model = RobertaForSequenceClassification.from_pretrained("your-folder")
    tokenizer = AutoTokenizer.from_pretrained("your-folder")
    # 初始化推理管道
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

    # 測試
    query = query
    # query = "在08:00:00 南勢角可以搭的車有哪幾班" 
    predicted_class = classifier(query)# 可用分類模型預測

    print(predicted_class)

    # 查詢語意相似問題，以下if可自行視需求修改
    if (predicted_class[0]["label"]) == 'LABEL_3':
        docs = f"暫時不支援以上問題:{query}"
        I = 801604
        return I
    else: 
        query_vector = embedding_model.embed_query(query)
        # 轉為numpy格式（FAISS 要求 float32）
        query_vector_np = np.array([query_vector], dtype="float32")
        D, I = index.search(query_vector_np, k=1)
    
        return I[0][0]

def res(i):
    import pymssql,json
    
    # 1. MSSQL 連線

    # 連線參數
    with open('json/sql.json','r') as file:
            data = json.load(file)

    server = data.get("server")
    user = data.get("user")
    password = data.get("pw")
    database = data.get("database")

    conn = pymssql.connect(server, user, password, database)

    # 2.用id取出問題、回答，輸入sql語法
    cursor = conn.cursor()

    cursor.execute(f"your-sql-select")
    row = cursor.fetchone()
    print(row)
    if row:
        print("問題:", row[1])
        print("回答:", row[2])
    else:
        print("找不到該筆資料")


    # 提交交易
    conn.commit()

    # 關閉連線
    cursor.close()
    conn.close()

    return row[1],row[2]

def res_ans(row1,row2):
    import json
    from google import genai

    # 使用LLM模型整理內容並回答
    with open('json/llm-gimini.json','r') as file:
            data = json.load(file)

    client = genai.Client(api_key=data.get('key'))

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="your-prompt"
    ) 

    return response.text


