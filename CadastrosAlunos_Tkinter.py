from cgitb import text
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from PIL import ImageTk, Image
import sqlite3

class userwindow():
    sqlite_var = 0
    theCursor = 0
    curItem = 0

    def refresh(self):
        self.update_tree()
        self.clear_entries()
        print("Limpando...")

    def search_record(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.theCursor.execute("SELECT * FROM students where name like ? or phone like ?",('%'+self.search_value.get()+'%','%'+self.search_value.get()+'%'))
            self.result = self.theCursor.fetchall()
            length=str(len(self.result))
            if length==0:
                messagebox.showinfo("NAO FOI POSSIVEL CADASTRAR")
            if length!=0:
                i=0
                for row in self.result:
                    if i%2==0:
                        self.tree.insert("",END, values=row,tag='1')
                    else:
                        self.tree.insert("",END, values=row,tag='2')
                    i=i+1
        except:
            raise
            print("NÃO FOI POSSÍVEL ENCONTRAR OS DADOS")

    def clear_entries(self):
        self.search_value.set("")

    def update_tree(self):#treeview
        try:
            self.tree.delete(*self.tree.get_children())
            self.theCursor.execute("SELECT * FROM students")
            self.rows = self.theCursor.fetchall()
            i=0
            for row in self.rows:
                if i%2==0:
                    self.tree.insert("",END,values=row,tag='1')
                else:
                    self.tree.insert("",END,values=row,tag='2')
                i=i+1
        except:
            print("NAO FOI POSSIVEL ENCONTRAR DADOS")

    def setup_db(self):
        try:
            self.sqlite_var = sqlite3.connect('student.db')
            self.theCursor = self.sqlite_var.cursor()
        except:
            print("NAO FOI POSSIVEL CONECTAR AO BANCO DE DADOS")

        try:
                self.theCursor.execute("CREATE TABLE if not exists students(ID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT UNIQUE NOT NULL, Phone TEXT NOT NULL, Endereco TEXT NOT NULL);")
        except:
                print("NAO FOI POSSIVEL CRIAR A TABELA")
        finally:
                self.sqlite_var.commit()
                self.update_tree()


    def __init__(self):
        self.user_window = Tk()
        self.user_window.resizable(False, False)
        self.user_window.iconbitmap("logo.ico")
        self.user_window.title("Cadastro de usuários")



        self.tree = ttk.Treeview(self.user_window, selectmode="browse", column=("column1","column2","column3", "column4"),show='headings')
        self.tree.column("column1", width=170, minwidth=170, stret=NO)
        self.tree.heading("#1", text="Acesso")
        self.tree.column("column2", width=170, minwidth=170, stret=NO)
        self.tree.heading("#2", text="Nome")
        self.tree.column("column3", width=170, minwidth=170, stret=NO)
        self.tree.heading("#3", text="Telefone")
        self.tree.column("column4", width=170, minwidth=170, stret=NO)
        self.tree.heading("#4", text="Endereço")
        self.tree.tag_configure('1',background='ivory2')
        self.tree.tag_configure('2',background='alice blue')
        self.tree.grid(row=4, column=0, columnspan=4, padx=9, pady=9, sticky=W+E)

        Label(self.user_window, text="Pesquisar por parte do nome ou pelo telefone:").grid(row=5, column=0,columnspan=2, sticky=E, padx=9, pady=9)
        self.search_value = StringVar(self.user_window, value="")
        Entry(self.user_window, textvariable = self.search_value).grid(row=5, column=2, padx=9, pady=9)
        self.search_button = ttk.Button(self.user_window, text="Pesquisar",command=self.search_record)
        self.search_button.grid(row=5, column=3, padx=9, sticky=W + E)

        self.refresh_button = ttk.Button(self.user_window,text="Atualizar", command=self.refresh)
        self.refresh_button.grid(row=6, column=3,padx=9,pady=9,sticky=W+E)
        Label(self.user_window, text="Desenvolvido por Thiago Fernando").grid(row=6, column=2, columnspan=2, sticky=W, padx=9, pady=9)



        self.setup_db()
        self.user_window.mainloop()


class adminwindow:
    sqlite_var = 0
    theCursor = 0
    curItem = 0

    def refresh(self):
        self.update_tree()
        self.clear_entries()
        print("Atualizar Dados")

    def search_record(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.theCursor.execute("select * from students where name like ? or phone like ?", ('%'+self.search_value.get()+'%','%'+self.search_value.get()+'%'))
            self.result = self.theCursor.fetchall()
            length=str(len(self.result))
            if length==0:
                messagebox.showinfo("Não foi possível encontrar nenhum resultado")
            if length!='0':
                i=0
                for row in self.result:
                    if i%2==0:
                        self.tree.insert("",END, values=row,tag='1')
                    else:
                        self.tree.insert("",END, value=row,tag='2')
                    i=i+1
        except:
            raise
            print("Não foi possível encontrar nenhum resultado")

    def reset_db(self):
        yesno=messagebox.askquestion("CUIDADO !! DESEJA REALMENTE APAGAR TODOS OS DADOS?")
        if yesno=='yes':
            self.theCursor.execute("DROP TABLE students")
            print("TODOS OS DADOS DO BANCO FORAM DELETADOS")
            self.setup_db()
            self.update_tree()

    def clear_entries(self):
        self.Name_entry.delete(0, "end")
        self.Phone_entry.delete(0, "end")
        self.Adress_entry.delete(0, "end")

    def delete_record(self):
        try:
            self.theCursor.execute("delete FROM students WHERE ID=?",(self.curItem['values'][0],))
            print("DADOS EXCLUIDOS")
        except:
            print("NAO FOI POSSIVEL EXCLUIR")
        finally:
            self.curItem=0
            self.clear_entries()
            self.update_tree()
            self.sqlite_var.commit()

    def update_record(self):
        if self.Name_value.get()!="" and self.Phone_value.get()!="" and self.Adress_value.get()!="":
            try:
                self.theCursor.execute("""UPDATE students SET name =?,phone=?, endereco=?, WHERE ID= ?""",
                                       (self.Name_value.get(), self.Phone_value.get(), self.Adress_value.get(), self.curItem['values'][0]))
                print("DADOS ATUALIZADOS")

            except sqlite3.IntegrityError:
                messagebox.showerror("DADOS JÁ EXISTEM")
            except:
                print("NAO FOI POSSÍVEL ATUALIZAR OS DADOS")
            finally:
                self.update_tree()
                self.sqlite_var.commit()
        else:
            messagebox.showwarning("FAVOR PREENCHER TODOS OS CAMPOS")

    def selectItem(self,event):
        self.curItem = self.tree.item(self.tree.focus())
        print(self.curItem)
        self.Name_value.set(self.curItem["values"][1])
        self.Phone_value.set(self.curItem["values"][2])
        self.Adress_value.set(self.curItem["values"][3])

    def update_tree(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.theCursor.execute("SELECT * FROM students")
            self.rows = self.theCursor.fetchall()
            i=0
            for row in self.rows:
                if i%2==0:
                    self.tree.insert("",END, values=row,tag='1')
                else:
                    self.tree.insert("",END, values=row,tag='2')
                i=i+1
        except:
            print("NÃO FOI POSSÍVEL ATUALIZAR OS DADOS")

    def write_record(self):
        if self.Name_value.get()!="" and self.Adress_value.get()!="" and self.Phone_value.get()!="":
            try:
                self.theCursor.execute("""INSERT INTO students (Name, Phone, Endereco) VALUES (?,?,?)""",
                (self.Name_value.get(),self.Phone_value.get(),self.Address_value.get()))
                self.sqlite_var.commit()
                self.theCursor.execute("SELECT *,max(id) FROM students")
                self.rows=self.theCursor.fetchall()
                print(self.rows[0][0],"{Name : ",self.rows[0][1],"| No : ",self.rows[0][2],"| Endereco :",self.rows[0][3],"} FOI CADASTRADO !")
                self.clear_entries()
            except sqlite3.IntegrityError:
                messagebox.showerror("ESTE DADO JÁ ENCONTRA-SE NO BANCO")
            except:
                print("NÃO FOI POSSIVEL ATUALIZAR OS DADOS")
            finally:
                self.update_tree()

        else:
            messagebox.showwarning("FAVOR PREENCHER TODOS OS CAMPOS")







    def __init__(self):
        self.admin_window = Tk()
        self.admin_window.title("Cadastro de usuários")
        self.admin_window.resizable(False, False)
        self.admin_window.iconbitmap("logo.ico")

        self.Name_Label = Label(self.admin_window, text="Nome")
        self.Name_Label.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        self.Name_value = StringVar(self.admin_window, value="")
        self.Name_entry = ttk.Entry(self.admin_window,textvariable=self.Name_value)
        self.Name_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky=W+E)


        self.Phone_Label = Label(self.admin_window, text="Telefone")
        self.Phone_Label.grid(row=1, column=0, sticky=W, padx=10, pady=10)
        self.Phone_value = StringVar(self.admin_window, value="")
        self.Phone_entry = ttk.Entry(self.admin_window,textvariable=self.Phone_value)
        self.Phone_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky=W+E)


        self.Adress_Label = Label(self.admin_window, text="Endereço")
        self.Adress_Label.grid(row=2, column=0, sticky=W, padx=10, pady=10)
        self.Andress_value = StringVar(self.admin_window, value="")
        self.Adress_entry = ttk.Entry(self.admin_window, textvariable=self.Andress_value)
        self.Adress_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky=W+E)


        self.submit_button = ttk.Button(self.admin_window, text="Cadastrar", command=self.write_record)
        self.submit_button.grid(row=0, column=3, padx=9, sticky=W+E)

        self.update_button = ttk.Button(self.admin_window, text="Atualizar", command=self.update_record)
        self.update_button.grid(row=1, column=3, padx=9, sticky=W + E)

        self.delete_button = ttk.Button(self.admin_window, text="Remover", command=self.delete_record)
        self.delete_button.grid(row=2, column=3, padx=9, sticky=W + E)

        self.tree = ttk.Treeview(self.admin_window, selectmode="browse", column=("column1","column2","column3", "column4"),show='headings')
        self.tree.column("column1", width=170, minwidth=170, stret=NO)
        self.tree.heading("#1", text="Acesso")
        self.tree.column("column2", width=170, minwidth=170, stret=NO)
        self.tree.heading("#2", text="Nome")
        self.tree.column("column3", width=170, minwidth=170, stret=NO)
        self.tree.heading("#3", text="Telefone")
        self.tree.column("column4", width=170, minwidth=170, stret=NO)
        self.tree.heading("#4", text="Endereço")
        ###############################################################################################
        self.tree.bind("<ButtonRelease-1>",self.selectItem)
        self.tree.bind("<space>",self.selectItem)
        self.tree.tag_configure('1', background='ivory2')
        self.tree.tag_configure('2', background='alice blue')
        ###############################################################################################
        self.tree.grid(row=4, column=0, columnspan=4, padx=9, pady=9, sticky=W+E)

        Label(self.admin_window, text="Pesquisar por parte do nome ou pelo telefone:").grid(row=5, column=0,columnspan=2, sticky=E, padx=9, pady=9)
        self.search_value = StringVar(self.admin_window, value="")
        Entry(self.admin_window, textvariable = self.search_value).grid(row=5, column=2, padx=9, pady=9)
        self.search_button = ttk.Button(self.admin_window, text="Pesquisar", command=self.search_record)
        self.search_button.grid(row=5, column=3, padx=9, sticky=W + E)

        Label(self.admin_window, text="Desenvolvido por").grid(row=6, column=2, columnspan=2, sticky=W, padx=9, pady=9)

        self.reset_button = ttk.Button(self.admin_window, text="Limpar banco de dados")
        self.reset_button.grid(row=5, column=3, padx=9, sticky=W + E)

        self.refresh_button = ttk.Button(self.admin_window,text="Atualizar", command=self.refresh)
        self.refresh_button.grid(row=6, column=2, padx=9,pady=9,sticky=W+E)


        Label(self.admin_window,text="Desenvolvido por Thiago Fernando").grid(row=6,column=0,pady=9,padx=9,sticky=W)
        self.reset_button = ttk.Button(self.admin_window,text="Limpar dados do banco - CUIDADO!", command=self.reset_db)
        self.reset_button.grid(row=6, column=3, padx=9,pady=9,sticky=W+E)


        self.setup_db()
        self.admin_window.mainloop()


class signinwindow:
    sqlite_var = 0
    theCursor = 0
    curItem = 0

    def setup_db(self):
        try:
            self.sqlite_var = sqlite3.connect('students.db')
            self.theCursor = self.sqlite_var.cursor()
        except:
            print("NAO FOI POSSIVEL CONECTAR AO BANCO DE DADOS")

        try:
                self.theCursor.execute("CREATE TABLE if not exists users(username TEXT UNIQUE NOT NULL, Phone TEXT NOT NULL;")
        except:
                print("NAO FOI POSSIVEL CRIAR A TABELA")
        finally:
                self.sqlite_var.commit()


    def user_tree_update(self):
        self.tree.delete(*self.tree.get_children())
        self.theCursor.execute("SELECT * FROM users")
        res =self.theCursor.fetchall()
        i=0
        for row in res:
            if i%2==0:
                self.tree.insert("",END, values=row,tag='1')
            else:
                self.tree.insert("",END, values=row,tag='2')
            i=i+1


    def clear_users(self):

        self.theCursor.execute("DROP TABLE users")
        self.setup_db()
        self.user_tree_update()

    def view_users(self):
        try:
            self.theCursor.execute("SELECT * FROM users")
            res=self.theCursor.fetchall()
        except:
            print("NÃO FOI POSSÍVEL CARREGAR OS DADOS DO BANCO")
        self.x = Tk()
        self.x.title("Lista de usuários")
        self.x.resizable(False, False)
        self.x.iconbitmap("logo.ico")

        self.tree = ttk.Treeview(self.x, selectmode="browse", column=("column1", "column2"), show='headings')

        self.tree.heading("#1", text="Usuários")
        self.tree.heading("#2", text="Senha")
        self.tree.tag_configure('1',background='yellow')
        self.tree.tag_configure('2', background='light green')
        self.tree.grid(row=0, column=0, columnspan=4, sticky = W+E, padx=9, pady= 9)
        Button(self.x,text="Limpar Usuários",command=self.clear_users()).grid(row=1, column=0, columnspan=4, sticky = W+E, padx=9, pady= 9)
        self.user_tree_update()
        self.x.mainloop()



    def new_user(self):
        try:
            if self.username_text.get()!="" and self.password_text_get()!="":
                self.theCursor.execute("INSERT INTO users(username,password) VALUES(?,?)",(self.username_text.get(),self.password_text.get()))
                self.signin_window.destroy()
                messagebox.showinfo("CADASTRO FEITO COM SUCESSO")
            else:
                messagebox.showwarning("FAVOR PREENCHER TODOS OS CAMPOS")

        except sqlite3.IntegrityError:
            messagebox.showerror("ESTE USUÁRIO JÁ EXISTE NO BANCO")
        except:
            print("NÃO FOI POSSÍVEL EFETUAR O CADASTRO")
        finally:
            self.sqlite_var.commit()
            self.theCursor.execute("SELECT * FROM users")
            res=self.theCursor.fetchall()
            self.username_text.set("")
            self.password_text.set("")






    def __init__(self):
        self.signin_window = Toplevel()
        self.signin_window.title("Cadastro de usuários")
        self.signin_window.resizable(False, False)
        self.signin_window.iconbitmap("logo.ico")

        Label(self.signin_window, text="Cadastro de Aluno", font="Arial").grid(row=0, column=0, sticky=W, padx=10)
        Label(self.signin_window, text="Usuário: ", font="Arial, 10", foreground='purple4').grid(row=1, column=0)
        Label(self.signin_window, text="Senha: ", font="Arial, 10").grid(row=2, column=0, pady=(0, 20))

        Entry(self.signin_window, font="Arial, 10").grid(row=1, column=1)
        Entry(self.signin_window, font="Arial, 10").grid(row=2, column=1, pady=(0, 20))

        user_add = Button(self.signin_window, text="Cadastrar", font="Arial, 11", background='white', command=self.new_user())
        user_add.grid(row=1, column=2, rowspan=2, padx=20, pady= (0,20))

        view_existing = Button(self.signin_window, text="Visualizar Cadastros", background='white', command=self.view_users)
        view_existing.grid(row=3, column=0, rowspan=2, columnspan=4, padx=20, pady=(0, 20),sticky=W+E)


        self.signin_window.mainloop()


class loginwindow:
    sqlite_var = 0
    theCursor = 0
    curItem = 0

    def setup_db(self):
        try:
            self.sqlite_var = sqlite3.connect('students.db')
            self.theCursor = self.sqlite_var.cursor()
        except:
            print("NAO FOI POSSIVEL CONECTAR AO BANCO DE DADOS")

        try:
            self.theCursor.execute(
                "CREATE TABLE if not exists users(username TEXT UNIQUE NOT NULL, Phone TEXT NOT NULL;")
        except:
            print("NAO FOI POSSIVEL CRIAR A TABELA")
        finally:
            self.sqlite_var.commit()




    def logg(self):
        try:
            self.theCursor.execute("SELECT * FROM users")
            res=self.theCursor.fetchall()
            flag=0
            for x in res:
                if self.var.get()==1 and self.username_text.get()==x[0] and self.password_text.get()==x[1]:
                    self.login_window.destroy()
                    userwindow()
                    flag=1
            if self.var.get()==2 and self.username_text.get()=="admin" and self.password_text.get()=="admin":
                self.login_window.destroy()
                adminwindow()
                flag=1
            if flag==0:
                messagebox.showinfo("FAVOR PREENCHER TODOS OS CAMPOS")
        except:
            print("ERRO AO LOGAR")
            raise
        finally:
            self.password_text.set("")
            self.username_text.set("")





class mainwindow:



    def create_login(self):
        try:
            loginwindow()
        except:
            raise Exception("Não foi possível criar o formulário de login")


    def create_signin(self):
        try:
            signinwindow()
        except:
            raise Exception("Não foi possível criar o formulário de login")

    def about_us(self):
        messagebox.showinfo("thiagosantostc10@gmail.com", """Este aplicativo foi criado para facilitar o gerenciamento dos detalhes de alunos e foi criado por
          \nthiagosantostc10@gmail.com\n\nProgramado em: \n\nPython\nSQLite\n\n""")

    def help(self):
        import os, webbrowser
        from urllib.request import pathname2url
        url = 'file:{}'.format(pathname2url(os.path.abspath('help.html')))
        webbrowser.open(url)



    def quit_window(self):
        if messagebox.askokcancel("Usuário", "Deseja Realmente sair?"):
            self.root.destroy()

    def __init__(self):
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.quit_window)
        self.root.iconbitmap("logo.ico")
        self.root.title("CADASTRO DE ALUNOS")
        self.img = ImageTk.PhotoImage(Image.open("logo.ico"))
        self.panel = Label(self.root, image=self.img)
        self.panel.grid(row=0, column=0)

        Label(self.root, text="Cadastro de Alunos", font="Times, 29", foreground='purple').grid(row=1, column=0,
                                                                                                sticky=W + E, padx=40)
        Label(self.root, text="Desenvolvido Por thiagosantostc10@gmail.com", font="Arial, 8").grid(row=4, column=0,
                                                                                                   columnspan=2,
                                                                                                   sticky=W + E,
                                                                                                   pady=80)
        Label(self.root, text="Por favor, faça seu login para continuar", font="Arial, 12").grid(row=2, column=0,
                                                                                                 columnspan=2,
                                                                                                 sticky=W + E, pady=5)

        self.btn = Button(self.root, text="LOGIN", command=self.create_login)
        self.btn.configure(width=18, height=2, foreground='white', background="purple3")
        self.btn.grid(row=3, column=0, columnspan=2, sticky='N', pady=10)

        self.menu_bar = Menu(self.root)
        self.menu_bar.add_separator()

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Cadastrar", command=self.create_signin)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Sair", command=self.quit_window)
        self.menu_bar.add_cascade(label="Opções", menu=self.file_menu)

        self.menu_bar.add_separator()

        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Ajuda", command=self.help)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Sobre", command=self.about_us)
        self.menu_bar.add_cascade(label="Ajuda", menu=self.help_menu)

        self.root.configure(menu=self.menu_bar)
        self.root.mainloop()



try:
    mainwindow()
except:
    raise Exception("ESTE FORMULÁRIO NÃO PODE SER CRIADO")
