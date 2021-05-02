import PyPDF2
import tkinter as tk
import tkinter.filedialog
import tkinter.simpledialog
class PDF_MERGE_GUI(tk.Frame):
    file_cnt = 1
    STANDARD_TEXT = "Selected files: \n"
    def __init__(self , master = None):
        tk.Frame.__init__(self,master = master)
        self.selected_files_v = None
        self.master = master
        self.master.title("PDF_MERGER")
        self.create_widgets()
        pass
    def create_widgets(self):
        self.BUTTON_FILE_SELECT = tk.Button(self.master, text = "Select Files", command = self.select_files)
        self.BUTTON_FILE_SELECT.place(relx = 0.25, rely = 0.25, anchor = tk.CENTER)
        self.BUTTON_RESET = tk.Button(self.master, text = "Reset", command = self.reset)
        self.BUTTON_RESET.place(relx = 0.5, rely = 0.25, anchor = tk.CENTER)
        self.BUTTON_MERGE = tk.Button(self.master, text = "Merge", command = self.selectPages)
        self.BUTTON_MERGE.place(relx = 0.75, rely = 0.25, anchor = tk.CENTER)
        self.var = tk.StringVar()
        NUMB_OF_CHARACERS_FILENAME = 500
        self.Message_Box = tk.Message(self.master, textvariable = self.var, width = NUMB_OF_CHARACERS_FILENAME)
        self.var.set(self.STANDARD_TEXT)
        Y_SPACES = 200
        self.Message_Box.grid(pady = Y_SPACES)
        pass
    def select_files(self):
        if self.selected_files_v == None:
            temp = list(tk.filedialog.askopenfilenames())
            temp.reverse()
            self.selected_files_v = temp
        else:
            temp = list(tk.filedialog.askopenfilenames())
            temp.reverse()
            self.selected_files_v.extend(temp)
            
        self.write_on_ui()
        pass
    def write_on_ui(self):
        for i in range(self.file_cnt - 1, len(self.selected_files_v)):
            file_name = self.selected_files_v[i].split('/')[-1] #Get last Element. That will be the File without the Path
            self.var.set(self.var.get() + str(self.file_cnt) + ". " + file_name + '\n')
            self.file_cnt += 1
        pass
    def reset(self):
        self.selected_files_v = None
        self.var.set(self.STANDARD_TEXT)
        self.file_cnt = 1
        pass
    def selectPages(self):
        if self.selected_files_v != None:
            self.range_pages = SelectNumbOfPages(self.selected_files_v, self.merge,self.master).range_pages
        pass
    def merge(self):
        if self.selected_files_v == None:
            
            pass
        else:
            output_file = tk.simpledialog.askstring("Enter", "<Output file>.pdf: ")
            if output_file != None and ".pdf" in output_file:
                number = self.selected_files_v[0].rfind('/')
                path = self.selected_files_v[0][:number + 1]
                path += output_file
                merger = PyPDF2.PdfFileMerger()
                cnt = 0
                pageNumber = 0
                cast_to_int = lambda range_index, split_index : int ( self.range_pages[range_index].split('-')[split_index] )
                for file in self.selected_files_v:
                    if cnt == 0:
                        border1 = cast_to_int(cnt, 0) - 1 # -1 because start with zero
                        border2 = cast_to_int(cnt, 1)  
                        range_ = (border1, border2)
                        merger.merge(pageNumber, file, pages = range_)
                        pageNumber = border2
                    else:
                        border1 = cast_to_int(cnt, 0) - 1 # -1 because start with zero
                        border2 = cast_to_int(cnt, 1)       
                        range_ = (border1, border2)
                        merger.merge(pageNumber, file, pages = range_)
                        pageNumber += border2
                        pass
                    cnt += 1
                merger.write(path)
                
                merger.close()
                pass
            else:
                pass
            
            
            
            pass
        pass

class SelectNumbOfPages(tk.Frame):
    def __init__(self, pdfs : list ,callback, master = None):
        self.master = master
        self.window = tk.Toplevel(self.master)
        self.window.resizable(width = False, height = False)
        self.pdfs = pdfs
        self.callback = callback
        self.range_pages = []
        self.numb_of_pdfs = []
        cnt = 1
        for files in self.pdfs:
            file_name = files.split('/')[-1] #Get last Element. That will be the File without the Path
            self.numb_of_pdfs.append( str(cnt) + ". " + file_name )
            cnt += 1
        
        self.create_widgets()
        pass
    def create_widgets(self):
        self.texts = []
        cnt = 0
        for pdf in self.numb_of_pdfs:
            label = tk.Label(self.window, text = pdf, width = len(pdf), anchor = tk.W)
            label.grid(row = cnt, sticky = tk.W)
            text = "Select Pages (Default all pages are selected)"
            label = tk.Label(self.window, text = text, width = len(text), anchor = tk.W)
            label.grid(row = cnt, column = 2, sticky = tk.W)
            number_of_pages = str(PyPDF2.PdfFileReader(self.pdfs[cnt]).getNumPages())
            output_text = "1-" + number_of_pages
            self.texts.append( tk.Text(self.window, height = 1, width = len(output_text)) )
            self.texts[-1].insert("0.0" ,output_text)
            self.texts[-1].grid(row = cnt, column = 3, sticky = tk.W)
            cnt += 1
        tk.Button(self.window, text = "Confirm", command = self.evaluate_pages).grid(row = cnt, column = 0, sticky = tk.W ) 
        pass
    def close(self):
        self.window.destroy()
        self.callback()
    def evaluate_pages(self):
        for texts in self.texts:
            self.range_pages.append( texts.get('0.0', 'end')[: -1] ) # '\n' is not needed
        self.close()

def main():
    root = tk.Tk()
    root.geometry("450x450")
    root.resizable(width = False, height = False)
    app = PDF_MERGE_GUI(root)
    app.mainloop()
    pass


if __name__ == "__main__":
    main()
    pass