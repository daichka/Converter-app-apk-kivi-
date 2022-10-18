import requests,time,traceback
from bs4 import BeautifulSoup

from ast import literal_eval
from kivy.app import App
from kivy.graphics import *
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from  kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from kivy.core.window import Window
Window.clearcolor = (15/255,57/255,34/255,1)
Window.title = "Конвертер"

def curencypars():
	try:
		link = 'http://www.finmarket.ru/currency/rates/?id=10088'
		B_response = requests.get(link)
		soup = BeautifulSoup(B_response.content, 'html.parser')
		a = str(soup.find('div', class_='center_column').findAll('table')[2]).split('"fs11"')[2:-1]
		arrive = []
		for i in a:
			for ii in i.split('tbody'):
				arrive.append(ii.split('>')[1].split('<')[0] + ':' + ii.split('>')[4].split('<')[0] + ':' +
							  ii.split('>')[9].split('<')[0])
		cbd = open('konverter.txt').read().splitlines()
		if cbd== []:
			cbd = "Currency:Currency"
		else:
			cbd = cbd[0]
		file = open('konverter.txt', 'w')
		file.write(cbd + '\n' + str([time.ctime(time.time())[4:-5]]+arrive))
		file.close()
	except:
		try:
			cbd = open('konverter.txt').read().splitlines()[1]
			arrive = ['No internet connection:y'] + literal_eval(cbd)
		except:
			arrive = ['No internet connection:n:,::']
	return arrive
class Mybutton(ButtonBehavior, Image):
    def __init__(self,w, **kwargs):
        super(Mybutton, self).__init__(**kwargs)
        try:
        	self.source = w
        except:
            pass
class konvertervApp(App):
	def build(self):
		self.icon = 'appicon'
		self.buttons = {}
		self.butonscalc = ['+','-','/','*','=']
		buttonscalc = {}
		gridlayout = GridLayout(cols=3)
		try:
			file = open('konverter.txt').read().splitlines()[0].split(':')
			self.buttoncurrencychose1 = file[0]
			self.buttoncurrencychose2 = file[1]
		except:
			self.buttoncurrencychose1 = 'Currency'
			self.buttoncurrencychose2 = 'Currency'
		self.textstr1 = '0'
		self.currencylabelup = Label(text='',font_size=20, markup=True)
		self.textcurrencyupdate(1)
		for i in range(10):
			if i == 9:
				but =Mybutton('trash',size_hint=[0.5,1])
				self.buttons[but]= 'C'
				but.bind(on_press=self.cbuttonfunc)
				but = Button(text='0',font_size=35,background_color=[43/255,165/255,100/255,1])
				self.buttons[but]= '0'
				but.bind(on_press=self.numberbuttonfunc)
				but = Mybutton('prev', size_hint=[0.5, 1])
				self.buttons[but] = 'backs'
				but.bind(on_press=self.backsbuttonfunc)
				but = Mybutton('calc',size_hint=[0.5, 1])
				self.buttons[but] = 'calc'
				but.bind(on_press=self.calcbuttonmenufunc)
				but = Button(text='.',font_size=35, size_hint=[0.5, 1],background_color=[186/255,181/255,17/255,1])
				self.buttons[but] = '.'
				but.bind(on_press=self.numberbuttonfunc)
			else:
				but = Button(text=str(i+1),font_size=35,background_color=[43/255,165/255,100/255,1])
				self.buttons[but]= str(i+1)
				but.bind(on_press=self.numberbuttonfunc)

		for i in self.butonscalc:
			buttonscalc[Button(text=str(i),font_size=35,background_color=[229/255,98/255,22/255,1])]= str(i)
		boxlayoutcbc = BoxLayout(size_hint=[1,0.3])
		boxlayout0o = BoxLayout(size_hint=[1, 0.4])
		for i,value in self.buttons.items():
			if value == 'C':
				boxlayoutcbc.add_widget(i)
			elif value == 'backs':
				boxlayoutcbc.add_widget(i)
			elif value == 'calc':
				boxlayoutcbc.add_widget(i)
			elif value == '0':
				boxlayout0o.add_widget(i)
			elif value == '.':
				boxlayout0o.add_widget(i)

			else:
				if value != 'Change':
					gridlayout.add_widget(i)
		self.boxlayoutcalc = BoxLayout(orientation='vertical',size_hint=[0.3,1])
		self.calcbuttons = {}
		for i,value in buttonscalc.items():
			self.calcbuttons[i]= value
			self.boxlayoutcalc.add_widget(i)
			i.bind(on_press=self.calcbuttonsfunc)
		boxlayout = BoxLayout(orientation='vertical')
		if self.buttoncurrencychose1 == '' and self.buttoncurrencychose2 != '':
			self.curency1 = Button(text='Currency',font_size=35,background_color=[43/255,165/255,100/255,1])
			self.curency2 = Button(text=self.buttoncurrencychose2,background_color=[43/255,165/255,100/255,1])
		elif self.buttoncurrencychose2 == '' and self.buttoncurrencychose1 != '':
			self.curency1 = Button(text=self.buttoncurrencychose1,background_color=[43/255,165/255,100/255,1])
			self.curency2 = Button(text='Currency',font_size=35,background_color=[43/255,165/255,100/255,1])
		elif self.buttoncurrencychose1 != '' and self.buttoncurrencychose2 != '':
			self.curency1 = Button(text=self.buttoncurrencychose1,background_color=[43/255,165/255,100/255,1])
			self.curency2 = Button(text=self.buttoncurrencychose2,background_color=[43/255,165/255,100/255,1])
		else:
			self.curency1 = Button(text='Currency',font_size=35,background_color=[43/255,165/255,100/255,1])
			self.curency2 = Button(text='Currency',font_size=35,background_color=[43/255,165/255,100/255,1])
		self.swap = Mybutton('swap')
		self.swap.bind(on_press=self.swapbuttonfunc)

		curencydropdown1 = DropDown()
		self.buttonsval1 ={}
		self.buttonsval2 = {}
		for i in self.val.keys(): 
		    btn = Button(text=i,size_hint_y=None)
		    self.buttonsval1[btn]=i
		    btn.bind(on_release=lambda btn: curencydropdown1.select(btn.text))
		    curencydropdown1.add_widget(btn)
		self.curency1.bind(on_release=curencydropdown1.open)
		curencydropdown1.bind(on_select=self.currencyfunc1)
		curencydropdown2 = DropDown()
		for i in self.val.keys(): 
		    btn = Button(text=i,size_hint_y=None)
		    self.buttonsval2[btn]=i
		    btn.bind(on_release=lambda btn: curencydropdown2.select(btn.text))
		    curencydropdown2.add_widget(btn)
		self.curency2.bind(on_release=curencydropdown2.open)
		curencydropdown2.bind(on_select=self.currencyfunc2)
		boxlcurrencybuttons = BoxLayout(orientation='vertical')
		boxlcurrencylabel = BoxLayout(orientation='vertical')
		boxlayoutupmenu = BoxLayout(size_hint=[1,0.7])
		self.strinptext1 = Label(text='0',font_size=35)
		self.strinptext2 =Label(text='0',font_size=35)
		boxlayoutcurrencyupdate = BoxLayout(size_hint=[1,0.2])

		curupdbutton = Mybutton('update',size_hint=[0.2,1])
		curupdbutton.bind(on_press=self.textcurrencyupdate)
		self.valnameses = DropDown()
		for i in self.valnames:
			texts = Button(text=i, size_hint_y=None)
			texts.bind(on_press=lambda btn: curencydropdown1.select(btn.text.split(' ')[0]))
			self.valnameses.add_widget(texts)
		self.currencylabelup.bind(on_ref_press=lambda x,y:self.valnameses.open(x))
		self.valnameses.bind(on_select=self.currencyfunc1)

		boxlayoutcurrencyupdate.add_widget(curupdbutton)
		boxlayoutcurrencyupdate.add_widget(self.currencylabelup)

		boxlcurrencybuttons.add_widget(self.curency1)
		boxlcurrencybuttons.add_widget(self.swap)
		boxlcurrencybuttons.add_widget(self.curency2)
		boxlcurrencylabel.add_widget(self.strinptext1)
		boxlcurrencylabel.add_widget(self.strinptext2)
		boxlayoutupmenu.add_widget(boxlcurrencybuttons)
		boxlayoutupmenu.add_widget(boxlcurrencylabel)
		self.boxlayoutcommon = BoxLayout()

		boxlayout.add_widget(boxlayoutupmenu)
		boxlayoutnum0o = BoxLayout(orientation='vertical',size_hint=[1,1])

		boxlayoutnum0o.add_widget(gridlayout)
		boxlayoutnum0o.add_widget(boxlayout0o)
		self.boxlayoutcommon.add_widget(boxlayoutnum0o)
		boxlayout.add_widget(boxlayoutcbc)
		boxlayout.add_widget(self.boxlayoutcommon)
		boxlayout.add_widget(boxlayoutcurrencyupdate)
		self.currencylabelup.canvas.add(Rectangle(pos=[(Window.width -(Window.width*20/100))*70/100+240,30],size=[70,70],source='currencynames'))
		print(Window.height)

		return boxlayout
	def currencyfunc1(self,hueta,currencystr):
		try:
			file = open('konverter.txt', 'w')
			file.write(currencystr + ':' + self.buttoncurrencychose2+'\n'+str(self.ss[1:]))
			file.close()
			self.curency1.text = currencystr
			self.buttoncurrencychose1=currencystr
			self.valnameses.dismiss(True)
			if self.textstr1 != '0':
				try:
					self.strinptext2.text = str((float(self.textstr1) * float(self.val[self.buttoncurrencychose1])) / float(
						self.val[self.buttoncurrencychose2]))
				except:
					pass
			print(self.ss)
			if self.ss[0].split(':')[0] != 'No internet connection':
				try:
					self.currencylabelup.text =self.currencytimeupdate[4:-5]+': 1 '+self.buttoncurrencychose1+' = '+str(round(float(self.val[self.buttoncurrencychose1])/ float(self.val[self.buttoncurrencychose2]),2))+' '+self.buttoncurrencychose2+'     [ref=     ]     [/ref]'
				except:
					self.currencylabelup.text =self.currencytimeupdate[4:-5]+':  1'+self.buttoncurrencychose1+' = Currency     [ref=     ]     [/ref]'
			else:
				try:
					self.currencylabelup.text ='           No internet connection\n'+self.ss[:2][1:][0]+': 1 '+self.buttoncurrencychose1+' = '+str(round(float(self.val[self.buttoncurrencychose1])/ float(self.val[self.buttoncurrencychose2]),2))+' '+self.buttoncurrencychose2+'     [ref=     ]     [/ref]'
				except:
					self.currencylabelup.text ='           No internet connection\n'+self.ss[:2][1:][0]+':  1'+self.buttoncurrencychose1+' = Currency     [ref=     ]     [/ref]'
		except:
			pass
	def currencyfunc2(self,hueta,currencystr):
		try:
			file = open('konverter.txt', 'w')
			file.write(self.buttoncurrencychose1 + ':' + currencystr+'\n'+str(self.ss[1:]))
			file.close()
			self.curency2.text = currencystr
			self.buttoncurrencychose2 = currencystr
			if self.textstr1 != '0':
				try:
					self.strinptext2.text = str((float(self.textstr1) * float(self.val[self.buttoncurrencychose1])) / float(
						self.val[self.buttoncurrencychose2]))
				except:
					pass

			if self.ss[0].split(':')[0] != 'No internet connection':
				self.currencylabelup.text =self.currencytimeupdate[4:-5]+': 1 '+self.buttoncurrencychose1+' = '+str(round(float(self.val[self.buttoncurrencychose1])/ float(self.val[self.buttoncurrencychose2]),2))+' '+self.buttoncurrencychose2+'     [ref=     ]     [/ref]'
			else:
				self.currencylabelup.text ='           No internet connection\n'+self.ss[:2][1:][0]+': 1 '+self.buttoncurrencychose1+' = '+str(round(float(self.val[self.buttoncurrencychose1])/ float(self.val[self.buttoncurrencychose2]),2))+' '+self.buttoncurrencychose2+'     [ref=     ]     [/ref]'
		except:
			pass
	def swapbuttonfunc(self,widget):
		try:
			file = open('konverter.txt', 'w')
			file.write(self.buttoncurrencychose2 + ':' + self.buttoncurrencychose1+'\n'+str(self.ss[1:]))
			file.close()
			x = self.buttoncurrencychose1
			self.buttoncurrencychose1 = self.buttoncurrencychose2
			self.curency1.text = self.buttoncurrencychose1
			self.buttoncurrencychose2 = x
			self.curency2.text = x
			if self.textstr1 != '0':
				try:
					self.strinptext2.text = str((float(self.textstr1) * float(self.val[self.buttoncurrencychose1])) / float(self.val[self.buttoncurrencychose2]))
				except:
					pass
			if self.ss[0].split(':')[0] != 'No internet connection':
				try:
					self.currencylabelup.text =self.currencytimeupdate[4:-5]+': 1 '+self.buttoncurrencychose1+' = '+str(round(float(self.val[self.buttoncurrencychose1])/ float(self.val[self.buttoncurrencychose2]),2))+' '+self.buttoncurrencychose2+'     [ref=     ]     [/ref]'
				except:
					self.currencylabelup.text =self.currencytimeupdate[4:-5]+':  Currency = Currency     [ref=     ]     [/ref]'
			else:
				try:
					self.currencylabelup.text ='           No internet connection\n'+self.ss[:2][1:][0]+': 1 '+self.buttoncurrencychose1+' = '+str(round(float(self.val[self.buttoncurrencychose1])/ float(self.val[self.buttoncurrencychose2]),2))+' '+self.buttoncurrencychose2+'     [ref=     ]     [/ref]'
				except:
					self.currencylabelup.text ='           No internet connection\n'+self.ss[:2][1:][0]+':  Currency = Currency     [ref=     ]     [/ref]'
		except:
			pass
	def cbuttonfunc(self,widget):
		self.textstr1 = '0'
		self.strinptext1.text = '0'
		self.strinptext2.text = '0'
	def backsbuttonfunc(self,widget):
		try:
			if self.textstr1 != '0':
				if len(self.textstr1) == 1:
					self.textstr1 = '0'
					self.strinptext1.text = '0'
					self.strinptext2.text = '0'
				else:
					self.textstr1 = self.textstr1[:-1]
					self.strinptext1.text = self.textstr1
					self.strinptext2.text = str((float(self.textstr1) * float(self.val[self.buttoncurrencychose1])) / float(self.val[self.buttoncurrencychose2]))
		except:
			pass
	def numberbuttonfunc(self,widget):
		try:
			if self.buttons[widget]=='.':
				if '.' not in list(self.textstr1):
					self.textstr1 += self.buttons[widget]
					self.strinptext1.text = self.textstr1
			else:
				if self.textstr1=='0':
					self.textstr1 = self.buttons[widget]
					self.strinptext1.text=self.textstr1
					self.strinptext2.text=str((float(self.textstr1)*float(self.val[self.buttoncurrencychose1]))/float(self.val[self.buttoncurrencychose2]))
				else:
					self.textstr1 += self.buttons[widget]
					self.strinptext1.text = self.textstr1
				self.strinptext2.text = str((float(self.textstr1) * float(self.val[self.buttoncurrencychose1])) / float(self.val[self.buttoncurrencychose2]))
		except:
			pass
	def textcurrencyupdate(self,govnoraz):
		try:
			self.val = {'AZN': '1'}
			ss = curencypars()
			self.ss = ss
			s = ss
			if s[0].split(':')[1] == 'y':

				t = s[:2][1:][0]
				print(s[:2][1:])
				s = s[2:]

				for i in s:
					self.val[i.split(':')[0]] = i.split(':')[2].split(',')[0] + '.' + i.split(':')[2].split(',')[1]
				self.valnames = ['AZN Азербайджанский манат']

				for i in s:
					self.valnames.append(i.split(':')[0] + ' ' + i.split(':')[1])
				print(s,self.val)
				self.currencytimeupdate = time.ctime(time.time())
				try:
					self.currencylabelup.text ='           No internet connection\n'+t+': 1 '+self.buttoncurrencychose1+' = '+str(round(float(self.val[self.buttoncurrencychose1])/ float(self.val[self.buttoncurrencychose2]),2))+' '+self.buttoncurrencychose2+'     [ref=     ]     [/ref]'
				except:
					print(traceback.format_exc())
					self.currencylabelup.text ='           No internet connection\n'+t+':  Currency = Currency     [ref=     ]     [/ref]'

			elif s[0].split(':')[1] == 'n':
				self.val = {}
				self.valnames = []
				for i in s:
					self.val[i.split(':')[0]] = i.split(':')[2].split(',')[0] + '.' + i.split(':')[2].split(',')[1]
				
				for i in s:
					self.valnames.append(i.split(':')[0] + ' ' + i.split(':')[1])
				self.currencytimeupdate = time.ctime(time.time())
				try:
					self.currencylabelup.text ='           No internet connection\n'+self.currencytimeupdate[4:-5]+': 1 '+self.buttoncurrencychose1+' = '+str(round(float(self.val[self.buttoncurrencychose1])/ float(self.val[self.buttoncurrencychose2]),2))+' '+self.buttoncurrencychose2+'     [ref=     ]     [/ref]'
				except:
					self.currencylabelup.text ='           No internet connection\n'+self.currencytimeupdate[4:-5]+':  Currency = Currency     [ref=     ]     [/ref]'

			else:
				for i in s:
					self.val[i.split(':')[0]] = i.split(':')[2].split(',')[0] + '.' + i.split(':')[2].split(',')[1]
				self.valnames = ['AZN Азербайджанский манат']
				for i in s:
					self.valnames.append(i.split(':')[0] + ' ' + i.split(':')[1])
				self.currencytimeupdate = time.ctime(time.time())
				try:
					self.currencylabelup.text =self.currencytimeupdate[4:-5]+': 1 '+self.buttoncurrencychose1+' = '+str(round(float(self.val[self.buttoncurrencychose1])/ float(self.val[self.buttoncurrencychose2]),2))+' '+self.buttoncurrencychose2+'     [ref=     ]     [/ref]'
				except:
					self.currencylabelup.text =self.currencytimeupdate[4:-5]+':  Currency = Curency     [ref=     ]     [/ref]'
		except:
			self.val = {}
			self.valnanames = []
	def calcbuttonmenufunc(self,widget):
		try:
			self.boxlayoutcommon.add_widget(self.boxlayoutcalc)
		except:
			self.boxlayoutcommon.remove_widget(self.boxlayoutcalc)
	def calcbuttonsfunc(self,widget):
		a = True
		for i in self.butonscalc:
			if self.textstr1[-1:] == i:
				a = False
		if a:
			if self.calcbuttons[widget] == '=':
				self.textstr1=str(eval(self.textstr1))
				self.strinptext1.text = self.textstr1
				self.strinptext1.text = self.textstr1
				self.strinptext2.text = str((float(self.textstr1) * float(self.val[self.buttoncurrencychose1])) / float(self.val[self.buttoncurrencychose2]))
			else:
				self.textstr1+=self.calcbuttons[widget]
				self.strinptext1.text=self.textstr1



if  __name__ == '__main__':
	konvertervApp().run()

