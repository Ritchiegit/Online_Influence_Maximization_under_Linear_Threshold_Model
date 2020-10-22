import os
def create_save_path(save_address):
    save_addressReward = save_address + "/Reward"
    save_addressRegret = save_address + "/Regret"
    save_addressParameterLoss = save_address + "/ParameterLoss"

    isExist = os.path.exists(save_address)
    if not isExist:
        os.makedirs(save_addressReward)
        os.makedirs(save_addressRegret)
        os.makedirs(save_addressParameterLoss)
        print("Created successfully")
    else:
        print("Directory already exists")
