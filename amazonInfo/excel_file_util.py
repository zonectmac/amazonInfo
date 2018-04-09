import sys, traceback
import xlrd, os
from xlwt import Workbook
from xlutils.copy import copy


def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(traceback.print_exc())


def write_excel_uk(save_path, uklist):
    book = Workbook()
    uksheet = book.add_sheet('uk')
    uksheet.col(0).width = 3000 * 2
    for rowindex, text in enumerate(uklist):
        uksheet.write(rowindex, 0, text)
    book.save(save_path)


def write_excel_de(save_path, delist):
    data = open_excel(save_path)
    wb = copy(data)
    wsuk = wb.get_sheet(0)
    wsuk.col(0).width = 3000 * 2
    wb.add_sheet('de')
    wsde = wb.get_sheet(1)
    wsde.col(0).width = 3000 * 2
    for rowindex, text in enumerate(delist):
        wsde.write(rowindex, 0, text)
    wb.save(save_path)
