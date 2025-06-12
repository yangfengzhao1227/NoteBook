def Cut(TextContent: str, WordDict: set) -> list:
    """
    执行智能分词的核心逻辑(修复版)
    :param TextContent: str - 需要分词的原始文本
    :param WordDict: set - 词库集合
    :return: list - 分词后的词汇列表
    
    算法流程：
    1. 基础分割 → 2. 单字检测 → 3. 增强最大匹配
    """
    # === 阶段1：改进型基础分割 ===
    WordBuffer, CurrentWord = list([]), str("")
    for Char in TextContent:
        # 仅中日韩字符连续合并（忽略标点影响）
        if '\u4e00' <= Char <= '\u9fff':
            CurrentWord += Char
        else:
            if CurrentWord:
                WordBuffer.append(CurrentWord)
                CurrentWord = str("")
            if Char not in [" ", "\n", "\t"]:
                WordBuffer.append(Char)
    if CurrentWord:
        WordBuffer.append(CurrentWord)
    
    # === 阶段2：增强型智能分词 ===
    OptimizedWords, Index = list([]), int(0)
    MaxWindow = int(6)  # 最大匹配窗口
    
    while Index < int(len(WordBuffer)):
        BestMatch = str("")
        # 动态计算匹配范围（防止越界）
        CurrentMax = min(MaxWindow, int(len(WordBuffer) - Index))
        
        # 逆向扫描找最长匹配
        for Length in range(CurrentMax, int(0), int(-1)):
            Candidate = str("").join(WordBuffer[Index:Index+Length])
            if Candidate in WordDict or Length == 1:  # 允许单字强制分割
                BestMatch = Candidate
                break
        
        # 处理未登录词（强制按单字分割）
        if BestMatch == str(""):
            BestMatch = WordBuffer[Index]
            OptimizedWords.append(BestMatch)
            Index += int(1)
        else:
            OptimizedWords.append(BestMatch)
            Index += int(len(BestMatch))
    
    return OptimizedWords
with open("zh-cn.txt", "r", encoding="utf-8") as ptr:
    # 读取词库文件并转换为集合
    word_dict = set(ptr.read().split())  # 假设词库用空格分隔
    
# 测试分词
input_text = input("请输入文本：")
print(Cut(input_text, word_dict))
