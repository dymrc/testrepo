#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 13:12:36 2019

@author: dongyeonchoi
"""
import sys
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QPushButton, QWidget, QTabWidget, QLineEdit, QTextBrowser, QGridLayout, QComboBox, QLabel, QTextEdit

import requests
from bs4 import BeautifulSoup


class DY(QTabWidget):
    def __init__(self, parent = None):
        super(DY, self).__init__(parent)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        
        self.addTab(self.tab1,"Indeed Search")
        self.addTab(self.tab2,"Bookmarked")
        
        self.searchtab()
        self.bookmarktab()
        
        self.setWindowTitle("Job Crawler")
        self.setGeometry(100, 100, 800, 800)
        self.show()
        
              
    def searchtab(self):
        layout = QGridLayout()
        self.enter = QLineEdit()
        self.enter.setPlaceholderText('Enter the Search Word')
        self.enter.returnPressed.connect(self.crawl_indeed)
        
        self.cb = QComboBox()
        self.cb.addItem('See All')
        self.cb.addItem('Internship')
        self.cb.addItem('Full-time')
        self.cb.addItem('Part-time')
        self.cb.activated[str].connect(self.onActivated)
        
        
        self.button = QPushButton('Serach')
        self.button.clicked.connect(self.crawl_indeed)
        
        self.label = QLabel('')
        self.label.resize(1,1)
        
        self.tb = QTextBrowser()
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)
        
        layout.addWidget(self.enter, 0, 0, 1, 3)
        layout.addWidget(self.cb, 0, 3, 1 ,1)
        layout.addWidget(self.button, 0, 4, 1, 1)
        layout.addWidget(self.label, 1, 0, 1, 5)
        layout.addWidget(self.tb, 2, 0, 1, 5)

        self.tab1.setLayout(layout)
        
        
    def onActivated(self, text):
        self.label.setText(text)
        self.label.adjustSize()

    def crawl_indeed(self):
        search_word = self.enter.text()
        search_filter = self.cb.currentText()

        if search_word:
            self.label.setText('Recently Added on Indeed for "' + search_word + '"')
            self.tb.clear()
            
            url_search = 'https://www.indeed.com/jobs?q='
            
            if search_filter == 'See All':
                url = url_search + search_word
            
            elif search_filter == 'Internship':
                url = url_search + search_word + '&jt=internship'
                
            elif search_filter == 'Full-time':
                url = url_search + search_word + '&jt=fulltime'
            
            elif search_filter == 'Part-time':
                url = url_search + search_word + '&jt=parttime'
            
            response = requests.get(url)
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            job = soup.select('#resultsCol > div > .title > a')
            comp = soup.select('#resultsCol > div > .sjcl > div > .company')
            loc = soup.select('#resultsCol > div > .sjcl > span')
                              
                                      
            for i in range(len(job)):                
                    title = job[i].text
                    company = comp[i].text
                    loca = loc[i].text
                    self.tb.append(str(i+1) + '. ' + title.strip() + '\n    ' + company.strip() + ', ' + loca.strip() +'\n')
                
                
                
    def bookmarktab(self):
        name = QLabel('Company Name:')
        nameedit = QLineEdit()
        location = QLabel('Location:')
        locedit = QLineEdit()
        note = QLabel('Note:')
        noteedit = QTextEdit()

        vbox = QVBoxLayout()
        vbox.addWidget(name)
        vbox.addWidget(nameedit)
        vbox.addWidget(location)
        vbox.addWidget(locedit)
        vbox.addWidget(note)
        vbox.addWidget(noteedit)
        vbox.addStretch()

        self.tab2.setLayout(vbox)
  
		
def main():
   app = QApplication(sys.argv)
   ex = DY()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()