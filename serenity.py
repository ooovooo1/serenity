# coding: utf-8
import re
import os

def clear_screen():
    os.system('cls')

def search_note_data(line,chname,totdkp,netdkp):
    if re.search('\[[^0-9]+\]',line):
        chname=line.split('"')[1]
    if re.search('\[1\]',line):
        totdkp=(line.strip().split(',')[0])
    if re.search('\[2\]',line):
        netdkp=(line.strip().split(',')[0])
    return (chname,totdkp,netdkp)

def search_alts_data(line):
    altch=mainch=''
    if re.search('\[[^0-9]+\]',line):
        altch=line.split('"')[1]
    if re.search('"[^0-9]+"',line):
        mainch=line.split('"')[3]
    return (altch,mainch)

def calculate_depth(line,depth):
    if re.search('{',line):
        depth+=1
    if re.search('}',line):
        depth-=1
    return depth

def process_lua_file(inFile):
    note_check=alts_check=depth=0
    chname=netdkp=totdkp=''
    while 1:
        line = inFile.readline()
        if not line: break
        if re.match('QDKP2note',line):
            note_check = 1
        if re.match('QDKP2_Alts',line):
            alts_check = 1
        depth=calculate_depth(line,depth)
        if not depth:
            note_check=0
        if note_check and depth==2:
            chname,totdkp,netdkp=search_note_data(line,chname,totdkp,netdkp)
        if chname and netdkp and totdkp:
            build_note_data(chname,totdkp,netdkp)
            chname=netdkp=totdkp=''
        if alts_check and depth==1:
            altch,mainch=search_alts_data(line)
            build_alts_data(altch,mainch)
    return data

def build_note_data(chname,totdkp,netdkp):
    data['QDKP2note'].update({chname:[(str(int(totdkp)-int(netdkp))),totdkp]})
    return

def build_alts_data(altch,mainch):
    if altch and mainch:
        data['QDKP2_Alts'].update({altch:mainch})
    return

def note_data_listing():
    for i in sorted(data['QDKP2note']):
        if i in data['QDKP2_Alts']:
            print ('%-30s Net:%-8s Tot:%s' %((i+' ('+data['QDKP2_Alts'][i]+' alt)'),data['QDKP2note'][i][0],data['QDKP2note'][i][1]))
        else:
            print ('%-30s Net:%-8s Tot:%s' %(i,data['QDKP2note'][i][0],data['QDKP2note'][i][1]))
    return

def note_data_search(chname):
    if chname in data['QDKP2note']:
        if chname in data['QDKP2_Alts']:
            print ('%s Net:%s Tot:%s' %((chname+' ('+data['QDKP2_Alts'][chname]+' alt)'),data['QDKP2note'][chname][0],data['QDKP2note'][chname][1]))
        else:
            print ('%s Net:%s Tot:%s' %(chname,data['QDKP2note'][chname][0],data['QDKP2note'][chname][1]))
    else:
        print ('Nem találtam ilyen karakter nevet!')
    return

def menu():
    while 1:
        clear_screen()
        print ('DKP lekérdezés:[1]')
        print ('Kilépés:[2]')
        print ('\n')
        menu_item=input('Válassz menüpontot: ')
        if menu_item == '1':
            while 1:
                clear_screen()
                print ('Keresés:[1]')
                print ('Listázás:[2]')
                print ('Vissza:[3]')
                print ('\n')
                menu_sub_item=input('Válassz menüpontot: ')
                if menu_sub_item == '1':
                    clear_screen()
                    chname=input('Karakter neve: ')
                    print ('\n')
                    note_data_search(chname)
                elif menu_sub_item == '2':
                    clear_screen()
                    note_data_listing()
                elif menu_sub_item == '3':
                    break
                print ('\n')
                input('Nyomj entert a továbblépéshez...')
        elif menu_item == '2':
            exit()
    return

inFile = open('QDKP_V2.lua',encoding='utf-8')
data={'QDKP2note':{},'QDKP2_Alts':{}}
data=process_lua_file(inFile)
inFile.close()
menu()

