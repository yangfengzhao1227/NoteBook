from MainModule import *
from SubModule import *
class NoteBook(object):
    def __init__(self):
        self.HotKeyDict=dict({})
        self.HelpDict=dict({})
        self.TabDict=dict({})
        self.CommandDict=dict({})
        self.TagList=list([])
        self.PluginList=list([])
        self.PassWordDict=set({})
        self.IgnoreWordDict=set({})
        self.PassDictPath=str("")
        self.IgnoreDictPath=str("")
        self.Version=str("")
        self.SnapShots=str("")
        self.CommandString=str("")
        self.TabNumber=int(1)
        self.ViewState=bool(True)
        self.DevlopmentState=bool(False)
        self.RootWindow=Tk()
        self.RootWindow.title("记事本")
        self.MainFont=Font(family="Consolas",size=10)
        self.MainFrame=Frame(self.RootWindow)
        try:
            windll.shcore.SetProcessDpiAwareness(1)
            self.RootWindow.tk.call("tk","scaling",windll.shcore.GetScaleFactorForDevice(0)/75)
        except Exception:
            pass
        Style().configure(".",foreground="#000000")
        Style().theme_use("vista")
        chdir(dirname(abspath(__file__)))
        self.TabBar=Notebook(self.MainFrame)
        self.HomePage=Frame(self.TabBar)
        self.Terminal=ScrolledText(self.HomePage,width=45,height=15,font=self.MainFont)
        self.Terminal.grid(row=0,column=0,columnspan=145,rowspan=10,sticky="nsew")
        self.Terminal.insert(End,"终端已准备就绪.工作已完成(746/746).\n>>>")
        self.Terminal.bind("<Key>",self.Command)
        self.HomePage.grid(sticky="nsew")
        self.EditorPage=Frame(self.TabBar)
        self.Text=ScrolledText(self.EditorPage,width=45,height=15,font=self.MainFont)
        self.Text.grid(sticky="nsew")
        self.TabBar.add(self.HomePage,text="主页")
        self.TabDict.update({self.TabBar.select():{"Text":self.Terminal,"Frame":self.HomePage,"Type":"HomePage"}})
        self.TabBar.add(self.EditorPage,text="标签页1")
        self.TabDict.update({self.TabBar.tabs()[-1]:{"Text":self.Text,"Frame":self.EditorPage,"Type":"EditorPage"}})
        self.TabNumber+=1
        self.TabBar.grid(row=1,column=0,sticky="nsew")
        self.TabBar.bind("<<NotebookTabChanged>>",self.ChangedTab)
        self.MenuBar=Menu(self.MainFrame)
        self.FileMenu=Menu(self.MenuBar,tearoff=False)
        self.FileMenu.add_command(label="打开",command=self.OpenFile)
        self.FileMenu.add_command(label="保存",command=self.SaveFile)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="隐藏",command=self.Iconify)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="重置",command=self.Reset)
        self.FileMenu.add_command(label="退出",command=self.Destroy)
        self.FileMenu.configure()
        self.MenuBar.add_cascade(label="文件",menu=self.FileMenu)
        self.EditMenu=Menu(self.MenuBar,tearoff=False)
        self.EditMenu.add_command(label="查找",command=self.FindWord)
        self.EditMenu.add_command(label="替换",command=self.ReplaceWord)
        self.EditMenu.add_separator()
        self.EditMenu.add_command(label="转到",command=self.GoTo)
        self.MenuBar.add_cascade(label="编辑",menu=self.EditMenu)
        self.OptionsMenu=Menu(self.MenuBar,tearoff=False)
        self.OptionsMenu.add_command(label="选项",command=self.Options)
        self.OptionsMenu.add_checkbutton(label="状态",command=self.View,variable=self.ViewState)
        self.OptionsMenu.add_separator()
        self.PluginsMenu=Menu(self.OptionsMenu,tearoff=False)
        self.PluginsMenu.add_command(label="选择",command=self.SelectPlugin)
        self.OptionsMenu.add_cascade(label="插件",menu=self.PluginsMenu)
        self.MenuBar.add_cascade(label="选项",menu=self.OptionsMenu)
        self.HelpMenu=Menu(self.MenuBar,tearoff=False)
        self.HelpMenu.add_command(label="帮助",command=self.Help)
        self.MenuBar.add_cascade(label="帮助",menu=self.HelpMenu)
        self.PopupMenu=Menu(self.RootWindow,tearoff=False)
        self.PopupMenu.add_command(label="剪切",command=self.Cut)
        self.PopupMenu.add_command(label="复制",command=self.Copy)
        self.PopupMenu.add_command(label="粘贴",command=self.Paste)
        self.PopupMenu.add_separator()
        self.FunctionMenu=Menu(self.PopupMenu,tearoff=False)
        self.FunctionMenu.add_command(label="时间",command=lambda:self.CurrentText.insert(Insert,strftime("%Y年%m月%d日 %H时%M分%S秒",localtime())))
        self.FunctionMenu.add_command(label="批注",command=lambda:self.CurrentText.insert(Insert,"批注:"))
        self.FunctionMenu.add_separator()
        self.TabsMenu=Menu(self.FunctionMenu,tearoff=False)
        self.TabsMenu.add_command(label="开启",command=self.CreatTab)
        self.TabsMenu.add_command(label="关闭",command=self.DeleteTab)
        self.FunctionMenu.add_cascade(label="标页",menu=self.TabsMenu)
        self.PopupMenu.add_cascade(label="功能",menu=self.FunctionMenu)
        self.PopupMenu.add_command(label="模型",command=self.Chat)
        self.RootWindow.bind("<Button-3>",self.ClickPopup)
        self.MainFrame.grid()
        self.RootWindow.configure(menu=self.MenuBar)
        self.CurrentText=self.Text
        self.Thread=Thread(target=self.ThreadFunction,daemon=True,name="SubThread")
        self.Thread.start()
        self.SetData()
        self.RootWindow.protocol("WM_DELETE_WINDOW",lambda:AskOkCancel("退出","是否退出?") and self.Destroy())        
        self.RootWindow.resizable(False,False)
        self.RootWindow.iconphoto(False,PhotoImage(file=dirname(abspath(__file__))+"\\Image\\Icon.png"))
        self.RootWindow.mainloop()
    def CutterWords(self,Context):
        def BidirectionalMaxMatch(Text,WordLength=6):
            def ForwardMatch(String):
                Result=list([])
                while String:
                    RangeLen=min(int(WordLength),int(len(String)))
                    for Index in range(RangeLen,int(0),int(-1)):
                        if String[:Index] in self.PassWordDict or Index==1:
                            Result.append(String[:Index])
                            String=String[Index:]
                            break
                return Result
            def BackwardMatch(String):
                Result=list([])
                while String:
                    RangeLen=min(int(WordLength),int(len(String)))
                    for Index in range(RangeLen,int(0),int(-1)):
                        if String[-Index:]in self.PassWordDict or Index==1:
                            Result.insert(0,String[-Index:])
                            String=String[:-Index]
                            break
                return Result
            return ForwardMatch(Text) if len(ForwardMatch(Text))<len(BackwardMatch(Text))else BackwardMatch(Text)
        return BidirectionalMaxMatch(Context)
    def Detect(self,Window):
        return windll.user32.GetParent(Window.winfo_id())
    def SetData(self):
        self.PassDictPath=dirname(abspath(__file__))+"\\Dict\\Chinese.txt"
        self.IgnoreDictPath=dirname(abspath(__file__))+"\\Dict\\Ignore.txt"
        self.Version="3"
        chdir(dirname(abspath(__file__)))
        self.HelpDict.update({"NoteBook-Coder使用指北":("","NoteBook-Coder是一个用于编辑文本/记录笔记的软件,我们允许使用插件优化NoteBook-Coder."),"文件类":("NoteBook-Coder使用指北","文件菜单提供了与文件操作相关的功能,如打开/保存/新建等."),"编辑类":("NoteBook-Coder使用指北","编辑菜单提供了文本编辑的常用功能,如查找/替换/检查等."),"选项类":("NoteBook-Coder使用指北","选项菜单提供了记事本的一些设置选项,如字体/颜色/自动保存等."),"打开":("文件类","点击此选项可以选择一个文本文件或日志文件打开,将文件内容显示在记事本中."),"保存":("文件类","点击此选项可以将当前记事本中的内容保存到指定的文件中."),"实例":("文件类","点击此选项可以创建一个新的记事本窗口."),"重置":("文件类","点击此选项可以关闭当前记事本窗口,并重新打开一个新的窗口."),"退出":("文件类","点击此选项可以关闭记事本程序."),"查找":("编辑类","点击此选项可以弹出查找窗口,输入要查找的文本,点击查找按钮进行查找."),"替换":("编辑类","点击此选项可以弹出替换窗口,输入要查找和替换的文本,点击替换按钮进行替换."),"检查":("编辑类","点击此选项可以检查文本中的拼写错误,并将错误的词汇标记为红色."),"选项":("选项类","点击此选项可以弹出选项窗口,进行记事本的一些设置."),"状态":("选项类","点击此选项可以查看当前记事本的状态,如字符数/词汇数/编码方案等."),"NoteBook-Coder使用指南":("","Plugin插件可以用来优化/增强NoteBook-Coder的功能,我们允许用户自行制作插件."),"制作":("NoteBook-Coder使用指南","在制作插件时,您应该了解Python与Tkinter的工作原理."),"使用":("NoteBook-Coder使用指南","在使用插件时,您应该了解插件的功能与用法.非官方的插件我们不予承担责任."),"卸载":("NoteBook-Coder使用指南","在删除插件时,由于技术原因,目前需要您手动前往程序根目录下的Plugin文件夹删除."),"Updates更新":("","这里收集了自从NoteBook-Coder-Coder从V0至V4(开发中)开始的大更新."),"快照":("Updates更新","NoteBook-Coder/Coder-V3正在开发的新功能,目前无法下载快照.不过,启用开发者模式可以使用Preview-Snapshots(预览快照).")})
        self.HotKeyDict.update({"<Control-o>":self.OpenFile,"<Control-s>":self.SaveFile,"<Control-h>":self.ReplaceWord,"<Control-f>":self.FindWord,"<Control-g>":self.GoTo,"<Control-p>":self.Options,"<Control-O>":self.OpenFile,"<Control-S>":self.SaveFile,"<Control-H>":self.ReplaceWord,"<Control-F>":self.FindWord,"<Control-G>":self.GoTo,"<Control-P>":self.Options,"<Key>":self.CheckText})
        self.CommandDict.update({"Calc":"eval(CommandString[5:].strip(\"\\n\"))","Echo":"CommandString[5:].strip(\"\\n\")","SnapShots":"self.SnapShots"})
        self.SnapShots="V3-Code7AB"
        with open(self.PassDictPath,"r",-1,"UTF-8")as FilePointer:
            for Element in FilePointer.read().split(" "):
                if len(Element)==1:
                    continue
                else:
                    self.PassWordDict.add(Element)
        with open(self.IgnoreDictPath,"r",-1,"UTF-8")as FilePointer:
            for Element in FilePointer.read().split(" "):
                self.IgnoreWordDict.add(Element)
        for Event,Target in self.HotKeyDict.items():
            self.RootWindow.bind(Event,lambda event,TargetFunction=Target:TargetFunction())
        self.SetPlugin()
    def OpenFile(self):
        Pointer=askopenfilename(title="打开",filetype=[("文本文件",["*.txt","*.log"]),("任意文件",["*.*"])])
        try:
            with open(Pointer,"r",-1,"UTF-8")as FilePointer:
                self.CurrentText.delete("1.0",End)
                self.CurrentText.insert(End,FilePointer.read())
        except FileNotFoundError as Error:
            ShowWarning("打开","未选择文件!")
        except Exception as Error:
            ShowWarning("打开",f"未知的错误!\n如下:{Error}")
    def SaveFile(self):
        Pointer=asksaveasfilename(title="保存",filetypes=[("文本文件",[".txt",".log"]),("任意文件",["*.*"])],defaultextension=".txt")
        try:
            with open(Pointer,"w",-1,"UTF-8")as FilePointer:
                FilePointer.write(self.CurrentText.get("1.0",End))
        except FileNotFoundError as Error:
            ShowWarning("保存","未指定文件!")
        except Exception as Error:
            ShowWarning("保存",f"未知的错误!\n如下:{Error}")   
    def Reset(self):
        self.Destroy()
        NoteBook()
    def Destroy(self):
        self.RootWindow.quit()
        self.RootWindow.destroy()
        exit()
    def Iconify(self):
        self.RootWindow.iconify()
    def Command(self,event):
        def Run(CommandString):
            return str(eval(self.CommandDict.get(self.CommandString.split(" ")[0])))
        if event.keysym=="Return":
            self.CommandString=self.Terminal.get(End+"-2l linestart",End+"-1c")
            if self.CommandString.startswith(">>>") or self.CommandString.startswith("..."):
                self.CommandString=self.CommandString[3:]
                self.Terminal.delete(End+"-1c",End)
                self.Terminal.insert(End,"\n正在抓取任务中...\n任务已开始.\n")
                try:
                    self.Terminal.insert(End,f"命令的输出:"+Run(self.CommandString)+"\n")
                except TypeError:
                    ShowInfo("错误","无效的命令!")
                self.Terminal.insert(End,"任务已结束.\n>>>")
                return "break"
        elif event.keysym=="BackSpace":
            CurrentPosition=self.Terminal.index(INSERT)
            LineStart=self.Terminal.index(Insert+" linestart")
            PromptEnd=f"{LineStart}+3c" if self.Terminal.get(LineStart,f"{LineStart}+3c")==">>>" else LineStart
            if self.Terminal.compare(CurrentPosition,"<=",PromptEnd):
                return "break"
        else:
            pass
    def CreatTab(self):
        if len(self.TabDict.keys())<=5:
            EditorPage=Frame(self.TabBar)
            Text=ScrolledText(EditorPage,width=45,height=15,font=self.MainFont)
            Text.grid(sticky="nsew")
            self.TabBar.add(EditorPage,text=f"标签页{self.TabNumber}")
            self.TabDict.update({self.TabBar.tabs()[-1]:{"Text":Text,"Frame":EditorPage,"Type":"EditorPage"}})
            self.TabBar.select(self.TabBar.tabs()[-1])
            self.TabNumber+=1
        else:
            ShowInfo("提示","一个窗口只能有5个标签页,如有需要请新建实例.")
    def DeleteTab(self):
        if len(self.TabDict.keys())>=2 and self.TabDict[self.TabBar.select()].get("Type")!="HomePage":
            del self.TabDict[self.TabBar.select()]
            self.TabBar.forget(self.TabBar.select())
        else:
            ShowWarning("警告","不可以关闭该标签页.")
    def ChangedTab(self,event):
        self.CurrentText=self.TabDict.get(self.TabBar.select(),{}).get("Text") if self.TabBar.select() in self.TabDict else self.Text
    def FindWord(self):
        StartPostion="1.0"
        StopPostion=End
        def Next():
            nonlocal StartPostion
            try:
                self.CurrentText.tag_remove("Find","1.0",End)
                StartPostion=self.CurrentText.search(WordEntry.get(),StartPostion,stopindex=StopPostion)
                if StartPostion:
                    self.CurrentText.tag_add("Find",StartPostion,f"{StartPostion}+{len(WordEntry.get())}c")
                    StartPostion=f"{StartPostion}+{len(WordEntry.get())}c"
                    self.CurrentText.tag_configure("Find",foreground="Blue")
                else:
                    pass
            except Exception:
                FindWordWindow.destroy()
        FindWordWindow=Toplevel()
        FindWordWindow.title("查找")
        FindWordWindow.resizable(False,False)
        FindWordWindow.iconphoto(False,PhotoImage(file=dirname(abspath(__file__))+"\\Image\\Find.png"))
        FindWordFrame=Frame(FindWordWindow)
        FindLabel=Label(FindWordFrame,text="查找的字符串:",font=self.MainFont)
        FindLabel.grid(row=0,column=0)
        WordEntry=Entry(FindWordFrame,font=self.MainFont,width=27)
        WordEntry.grid(row=0,column=1,sticky="nsew")
        FindButton=Button(FindWordFrame,text="查找",command=Next)
        FindButton.grid(row=0,column=2)
        FindWordFrame.grid()
    def ReplaceWord(self):
        StartPostion="1.0"
        StopPostion=End
        def Next():
            nonlocal StartPostion
            try:
                StartPostion=self.CurrentText.search(WordEntryFind.get(),StartPostion,stopindex=StopPostion)
                if StartPostion:
                    self.CurrentText.tag_add("Replace",StartPostion,f"{StartPostion}+{len(WordEntryFind.get())}c")
                    self.CurrentText.delete(StartPostion,f"{StartPostion}+{len(WordEntryFind.get())}c")
                    self.CurrentText.insert(StartPostion,f"{WordEntryReplace.get()}")
                else:
                    pass
            except Exception:
                ReplaceWordWindow.destroy()
        ReplaceWordWindow=Toplevel()
        ReplaceWordWindow.title("替换")
        ReplaceWordWindow.resizable(False,False)
        ReplaceWordWindow.iconphoto(False,PhotoImage(file=dirname(abspath(__file__))+"\\Image\\Replace.png"))
        ReplaceWordFrame=Frame(ReplaceWordWindow)
        FindLabel=Label(ReplaceWordFrame,text="查找的字符串:",font=self.MainFont)
        FindLabel.grid(row=0,column=0)
        WordEntryFind=Entry(ReplaceWordFrame,font=self.MainFont,width=20)
        WordEntryFind.grid(row=0,column=1,sticky="nsew")
        ReplaceLabel=Label(ReplaceWordFrame,text="替换的字符串:",font=self.MainFont)
        ReplaceLabel.grid(row=1,column=0)
        WordEntryReplace=Entry(ReplaceWordFrame,font=self.MainFont,width=20)
        WordEntryReplace.grid(row=1,column=1,sticky="nsew")
        ReplaceButton=Button(ReplaceWordFrame,text="替换",command=Next)
        ReplaceButton.grid(row=0,column=2,columnspan=2)
        ReplaceWordFrame.grid()
    def GoTo(self):
        def GoToLine(LineNumber:int):
            try:
                self.CurrentText.mark_set(Insert,f"{LineNumber}.0")
                self.CurrentText.focus_force()
                self.CurrentText.see(Insert)
            except Exception:
                ShowError("跳转","没有发现新的行.")
        GoToWindow=Toplevel()
        GoToWindow.title("跳转")
        GoToWindow.resizable(False,False)
        GoToWindow.iconphoto(False,PhotoImage(file=dirname(abspath(__file__))+"\\Image\\GoTo.png"))
        GoToFrame=Frame(GoToWindow)
        LineLabel=Label(GoToFrame,text="行号:",font=self.MainFont)
        LineLabel.grid(row=0,column=0)
        LineEntry=Entry(GoToFrame,font=self.MainFont,width=20)
        LineEntry.grid(row=0,column=1,sticky="nsew")
        GoToButton=Button(GoToFrame,text="跳转",command=lambda:GoToLine(int(LineEntry.get())))
        GoToButton.grid(row=0,column=2)
        GoToFrame.grid()
    def CheckText(self):
        if self.CurrentText!=self.Terminal:
            def PreProcess(Text):
                Buffer,Current=list([]),list([])
                for Char in Text:
                    if Char.isalnum():
                        if Current and not Current[-1].isalnum():
                            Buffer.append(str("").join(Current))
                            Current=list([])
                        Current.append(Char)
                    elif "\u4e00"<=Char<="\u9fff":
                        if Current and Current[-1].isalnum():
                            Buffer.append(str("").join(Current))
                            Current=list([])
                        Current.append(Char)
                    else:
                        if Current:
                            Buffer.append(str("").join(Current))
                            Current=list([])
                        Buffer.append(Char)
                if Current:
                    Buffer.append(str("").join(Current))
                return Buffer
            TextContent=str(self.CurrentText.get("1.0",END))
            self.CurrentText.tag_remove("Check","1.0",END)
            CurrentPos=str("1.0")
            for Segment in PreProcess(TextContent):
                if len(Segment)==1 and not Segment.isalnum():
                    CurrentPos=f"{CurrentPos}+1c"
                    continue
                if search(r"^(https?|ftp)://|[\w.-]+@|^\d+$",Segment):
                    CurrentPos=f"{CurrentPos}+{int(len(Segment))}c"
                    continue
                for Word in self.CutterWords(Segment):
                    WordLen=int(len(Word))
                    EndPos=f"{CurrentPos}+{int(WordLen)}c"
                    if Word not in self.PassWordDict and Word not in self.IgnoreWordDict:
                        self.CurrentText.tag_add("Check",CurrentPos,EndPos)
                    CurrentPos=EndPos
            self.CurrentText.tag_configure("Check",foreground="Red")
            self.CurrentText.tag_raise("Check")
        else:
            pass
    def Cut(self):
        self.CurrentText.event_generate("<<Cut>>")
    def Copy(self):
        self.CurrentText.event_generate("<<Copy>>")
    def Paste(self):
        self.CurrentText.event_generate("<<Paste>>")
    def ClickPopup(self,event):
        self.PopupMenu.post(event.x_root,event.y_root)
    def Options(self):
        def ChangeBackGroundColor(Tuple):
            self.CurrentText.configure(background=Tuple[1])
        def ChangeForeGroundColor(Tuple):
            self.CurrentText.configure(foreground=Tuple[1])
        def ChangeFontName(FontName):
            self.MainFont.configure(family=FontName)
        def ChangeFontSize(FontSize):
            self.MainFont.configure(size=int(FontSize))
        OptionsWindow=Toplevel()
        OptionsWindow.title("选项")
        OptionsWindow.resizable(False,False)
        OptionsWindow.iconphoto(False,PhotoImage(file=dirname(abspath(__file__))+"\\Image\\Setting.png"))
        OptionsFrame=Frame(OptionsWindow)
        OptionsNoteBook=Notebook(OptionsFrame)
        NormalFrame=Frame(OptionsNoteBook)
        FontLabelFrame=LabelFrame(NormalFrame,text="字体设置")
        FontNameTipLabel=Label(FontLabelFrame,text="字体名称:")
        FontNameTipLabel.grid(row=0,column=0,pady=4)
        FontNameComboBox=Combobox(FontLabelFrame,value=families())
        FontNameComboBox.grid(row=0,column=1,pady=4)
        FontNameComboBox.bind("<<ComboboxSelected>>",lambda event:ChangeFontName(FontNameComboBox.get()))
        FontNameComboBox.set(self.MainFont.cget("family"))
        FontSizeTipLabel=Label(FontLabelFrame,text="字体尺寸:")
        FontSizeTipLabel.grid(row=1,column=0,pady=4)
        FontSizeComboBox=Combobox(FontLabelFrame,values=[Size for Size in range(10,96)])
        FontSizeComboBox.grid(row=1,column=1,pady=4)
        FontSizeComboBox.bind("<<ComboboxSelected>>",lambda event:ChangeFontSize(FontSizeComboBox.get()))
        FontSizeComboBox.set(self.MainFont.cget("size"))
        FontLabelFrame.grid(row=0,columnspan=2,sticky="nsew")
        ColorFrame=LabelFrame(NormalFrame,text="颜色设置")
        BackGroundColorButton=Button(ColorFrame,text="选取背景颜色",width=30,command=lambda:ChangeBackGroundColor(AskColor(title="选取")))  
        BackGroundColorButton.grid(row=2,columnspan=2,sticky="nsew",pady=2)
        ForeGroundColorButton=Button(ColorFrame,text="选取字体颜色",width=30,command=lambda:ChangeForeGroundColor(AskColor(title="选取")))
        ForeGroundColorButton.grid(row=3,columnspan=2,sticky="nsew",pady=2)
        ColorFrame.grid(row=1,columnspan=2,sticky="nsew")
        NormalFrame.grid(sticky="nsew")
        OptionsNoteBook.add(NormalFrame,text="一般设置")
        SuperFrame=Frame(OptionsNoteBook)
        TipLabel=Label(SuperFrame,text="\t\t等待新功能...")
        TipLabel.grid(sticky="nsew")
        SuperFrame.grid(sticky="nsew")
        SuperFrame.grid_rowconfigure(0,weight=1)
        SuperFrame.grid_columnconfigure(0,weight=1)
        OptionsNoteBook.add(SuperFrame,text="高级设置")
        OptionsNoteBook.grid(row=0,column=0,sticky="nsew")
        OptionsFrame.grid(sticky="nsew")
    def SetPlugin(self):
        def RunPlugin(FileName:str):
            with open(FileName,"r",-1,"UTF-8")as PluginPointer:
                Limit=dict({"__builtins__":{"open":open,"print":print,"input":input,"exec":exec,"str":str,"int":int,"float":float,"list":list,"tuple":tuple,"dict":dict,"set":set,"bool":bool,"len":len,"all":all,"any":any},"Text":self.CurrentText,"End":End})
                PluginName=FileName.split("\\")[-1].split(".")[0]
                PluginThread=Thread(target=lambda:exec(PluginPointer.read(),Limit,{}),daemon=True,name=f"PluginThread-{PluginName}")
                PluginThread.start()
        def PutPlugin(PluginName:str,PluginFile:str):
            if len(self.PluginList)==1:
                self.PluginsMenu.add_separator()
            else:
                pass
            with open(dirname(abspath(__file__))+"\\Plugin\\"+PluginFile,"r",-1,"UTF-8")as FilePointer:
                if FilePointer.read().split("\n")[0] in [""]:
                    RunPlugin(dirname(abspath(__file__))+"\\Plugin\\"+PluginFile)
                else:
                    self.PluginsMenu.add_command(label=PluginName,command=lambda:RunPlugin(dirname(abspath(__file__))+"\\Plugin\\"+PluginFile))
        for PluginFile in listdir(dirname(abspath(__file__))+"\\Plugin\\"):
            if PluginFile.endswith(".plg-pkg"):
                self.PluginList.append(PluginFile.split(".")[0])
                PutPlugin(PluginFile.split(".")[0],PluginFile)
            else:
                pass
    def SelectPlugin(self):
        def Finish():
            copyfile(Directory+"\\"+PluginNameComboBox.get()+".plg-pkg",dirname(abspath(__file__))+"\\Plugin\\"+PluginNameComboBox.get()+".plg-pkg")
            PluginWindow.destroy()
            self.Reset()
        Directory=str(askdirectory(title="插件"))
        PluginWindow=Toplevel()
        PluginWindow.title("插件")
        PluginWindow.resizable(False,False)
        PluginFrame=LabelFrame(PluginWindow,text="插件")
        PluginNameLabel=Label(PluginFrame,text="请选择插件:")
        PluginNameLabel.grid(row=0,column=0)
        PluginNameComboBox=Combobox(PluginFrame,values=[PluginFile.split(".")[0] for PluginFile in listdir(Directory) if PluginFile.endswith(".plg-pkg")])
        PluginNameComboBox.grid(row=0,column=1)
        PluginNameComboBox.bind("<<ComboboxSelected>>",lambda event:Finish())
        PluginFrame.grid(sticky="nsew")
    def Chat(self):
        def Link(ChatString):
            Url="https://openrouter.ai/api/v1/chat/completions"
            Headers={"Authorization":"Bearer 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","Content-Type":"application/json","HTTP-Referer":"<YOUR_SITE_URL>","X-Title":"<YOUR_SITE_NAME>"}
            Payload={"model":"deepseek/deepseek-r1-0528:free","messages":[{"role":"user","content":ChatString}],"temperature":0.7,"max_tokens":100000}
            try:
                Data=dumps(Payload).encode('utf-8')
                Req=Request(Url,data=Data,headers=Headers,method='POST')
                Context=create_default_context()
                with urlopen(Req,timeout=15,context=Context)as Response:
                    StatusCode=Response.status
                    ResponseData=Response.read().decode('utf-8')
                if StatusCode != 200:
                    return f"HTTP错误({StatusCode})\n响应内容:\n{ResponseData[:500]}"
                try:
                    Result=loads(ResponseData)
                except JSONDecodeError as Error:
                    return f"JSON解析失败(位置:{Error.pos})\n原始数据:\n{ResponseData[:500]}"
                if 'choices' not in Result or not Result['choices']:
                    raise ValueError("无效的响应结构")
                Answer=Result['choices'][0].get('message',{}).get('content','')
                return f"{Answer}\n"
            except HTTPError as Error:
                return f"HTTP错误({Error.code})\n原因:{Error.reason}\n详情:{Error.read()}"
            except URLError as Error:
                return f"网络错误:{Error.reason}\n建议检查网络连接"
            except TimeoutError:
                return "请求超时\n建议:检查网络或增大超时时间"
            except Exception as Error:
                return f"未知错误:\n{str(Error)}"
        ChatWindow=Toplevel()
        ChatWindow.title("模型")
        ChatWindow.resizable(False,False)
        ChatFrame=Frame(ChatWindow)
        TipsLabel=Label(ChatFrame,text="对话:")
        TipsLabel.grid(row=0,column=0,sticky="nsew")
        ChatEntry=Entry(ChatFrame)
        ChatEntry.grid(row=0,column=1,sticky="nsew")
        ChatButton=Button(ChatFrame,text="确定",command=lambda:self.Terminal.insert(End,"\n"+Link(ChatEntry.get())))
        ChatButton.grid(row=0,column=2,sticky="nsew")
        ChatFrame.grid()
    def View(self):
        if self.ViewState==True:
            Length=len(self.CurrentText.get("1.0",End))-1
            ShowInfo("统计",f"共有{Length}个字符.编码方案:UTF-8.")
        else:
            pass
        self.ViewState=not self.ViewState
    def Help(self):
        def ShowHelp():
            HelpText.configure(state=Normal)
            HelpText.delete("1.0",End)
            HelpText.insert(End,self.HelpDict.get(HelpTreeView.item(HelpTreeView.selection()).get("text"),"")[1])
            HelpText.configure(state=Disabled)
        HelpWindow=Toplevel()
        HelpWindow.title("帮助")
        HelpWindow.resizable(False,False)
        HelpWindow.iconphoto(False,PhotoImage(file=dirname(abspath(__file__))+"\\Image\\Info.png"))
        HelpFrame=Frame(HelpWindow)
        HelpTreeView=Treeview(HelpFrame,height=7)
        HelpTreeView.grid(row=0,column=0)
        Style().configure("Treeview",rowheight=21)
        HelpTreeView.column("#0",width=195)
        HelpText=ScrolledText(HelpFrame,width=25,height=7,font=self.MainFont)
        HelpText.grid(row=0,column=1,sticky="nsew")
        HelpFrame.grid()
        for Name,(Parent,_) in self.HelpDict.items():
            if Parent=="":
                HelpTreeView.insert("","end",iid=Name,text=Name)
            else:
                HelpTreeView.insert(Parent,"end",iid=Name,text=Name)
        HelpTreeView.bind("<<TreeviewSelect>>",lambda event:ShowHelp())
    def ThreadFunction(self):
        pass
NoteBook()
