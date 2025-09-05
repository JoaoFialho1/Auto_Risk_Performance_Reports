from src.assistants.read_portfolio import read
from src.complete_report import general_report

#==============Inputs==============#
start = '2025-04-01'
portfolio = 'portfolio1'


#============Read-Datas============#
p1_t, p1_w = read(f"inputs/{portfolio}.xlsx")


#==========Generate-Reports=========#
p1_report = general_report(p1_t, p1_w, start, portfolio_inicial_value=100000000)