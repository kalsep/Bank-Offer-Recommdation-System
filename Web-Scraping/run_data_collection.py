from config import *
from scb import *
from pnb import *  
from iob import *  

if __name__=="__main__":
    print("Startig Data Collection for IOB")
    iob_df = run_iob_offer()  # noqa: F405
    print("Completed IOB")
    print("Startig Data Collection for PNB")
    pnb_df = run_pnb_offers()  # noqa: F405
    print("Completed PNB")
    print("Startig Data Collection for SCB")
    scb_df = run_scb_offers()  # noqa: F405
    print("Completed SCB")
    consolidated_df = pd.concat([iob_df,pnb_df,scb_df])
    print("Saving The dataframe")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    consolidated_df.to_excel(f"consolidated_data{current_time}.xlsx")