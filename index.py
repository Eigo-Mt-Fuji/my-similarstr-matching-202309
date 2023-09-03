import gzip

def gzip_search(query: str, candidate_chunks: list[str], top_k: int=1):
    """
    文字列ベースで類似したテキストチャンクを推定するアルゴリズム.
    `query`, `chunk`, および`query + " " + chunk`をそれぞれgzipで圧縮し、編集距離のようなものをベースに評価する.
    Parameters:
        query (str): 検索クエリとして使用する文字列.
        top_k (int, optional): 返される類似チャンクの上位k個を指定する (default: 1).
    Returns:
        List[str]: 最も類似したテキストチャンクのリスト.
    ---
    Reference:
    -   “Low-Resource” Text Classification: A Parameter-Free Classification Method with Compressors (Jiang et al., Findings 2023)
        https://aclanthology.org/2023.findings-acl.426/
    """

    # 圧縮: query => Q
    Q = gzip.compress(query.encode())

    distance_from_Q = {}
    for chunk in candidate_chunks:
        # 圧縮: chunk => C (上記のquery => Qと同様)
        C = gzip.compress(chunk.encode())

        # queryとchunkを連結する
        query_chunk = query + " " + chunk
        # 共通事項をまとめて表現できるため、この値が小さいほど意味が近いということになる
        Q_C = gzip.compress(query_chunk.encode())

        # 編集距離の計算と似た形で、比較する文字列の長さを正規化する
        normalized_distance = (len(Q_C) - min(len(Q), len(C))) / max(len(Q), len(C))
        distance_from_Q[chunk] = normalized_distance

    # 最も近い`top_k`個までのチャンクを取得する
    return sorted(distance_from_Q, key=distance_from_Q.get)[:top_k]
    
# 疑似ローカルデータ
candidate_chunks = [
    "◯◯API",
]

query = "XXAPI実装"
closest = gzip_search(query, candidate_chunks, top_k=1)
print(closest)
