'''                                                                           
             ....  .... ....                           OpenTruth Presents                        
           ....=.. .--...:..                                     Oct 2024      
       .....=:.-:..-.-..::-                                                   
        .::.:::::-..:::.-.=.                                                  
     .. .:::.:::-:-:.::.-.-.                                                  
     .-:..::.-:-:-=.=:::-:=.                                         
       -.:-.:-.---.==:=:-=.-..                                   ...          
     ..-::-::----:-+--::=.+:-...                            ......::....      
       :-...--=----=----::----:.                            ..-..:::..-.      
       .::::---:::--:=-:.--=::--.                          ..:-.::-.:-:..     
       ..::.:::---:::---::-:-:.---:                      ::::-::--.:-::-.     
        .:-..::::-:::---::.-:-::...:.               ..:::-.=:--=-:-:::-:.     
        ..::..........---:.-::::- .:.             .:-::-:::::..:---:::..      
          ..=-:........-:...-::.-..::        ...==:::-::....:---=-:..         
          ...=---:..--:.=-:.-:-:.:.::..  ....:-:::-::......-:....             
            ..--:...--::-==::-:=-.:..-....:-::::::.. ....-..                  
            ...:-:..:-:::.:-:--:::.::.-::---:::.... ..::...                   
               ..:-:.-:.::::--:--:::....:---:.......::..                      
                 ...---::-.-:---.--::-..:....:.::::-..                        
                   ....::::.:::----:--:=:.............::..                    
                        .:-=.::..-:-..:=:...::.:..  .:::-..                   
                           .:-::-=:.. .=::....::-----=-:.:.                   
                           ...:-:.......-:=-:::-.      .--.                   
                          ..::............:====..        ..                   
             ..:::----::::.-*=:..:.   .-:...-:.                               
             ...-....-::....=-:.=..   .=.:-::.                                
             ..-:.....-:..:*+:..#-.  .==....-.                                
             ...-:::...::.-..-+=*.. .--.....-.                                
               ...=+=-::-:::.:::-+=:::.*....-.                                
                  .--=-:-:-.::--.--=-:..=----....                             
                   ...:---::=-=.....::.:::.:::.:...                           
                        ........  .:=.-::--:-=:--:..                          
                                  .:::--...--.:-:=:.                          
                                  ...... .....::....                          
                                               ..                             
'''                                                                                                              
import os
import sys
sys.path.append(os.path.abspath('.'))
import time

from interface.actionInterface import actionInterface
from interface.decisionInterface import decisionInterface
from interface.dialogManagerInterface import dialogManagerInterface
from interface.memoryInterface import memoryInterface
from interface.aiBridgeInterface import aiBridgeInterface
from interface.observationInterface import observationInterface

from src.actionX import actionX
from src.decision import decision
from src.dialogManager import dialogManager
from src.memory import memory
from src.observationX import observationX
from src.logs import logs
from src.gpt import gpt

from src.config import get_config
config=get_config()


class openTruth:
    def __init__(self, action_instance: actionInterface, decision_instance: decisionInterface, dialogManager_instance: dialogManagerInterface, memory_instance: memoryInterface, observation_instance: observationInterface, logs_instance: logs, gpt_instance: aiBridgeInterface):
        self.action = action_instance
        self.decision = decision_instance
        self.dialogManager = dialogManager_instance
        self.memory = memory_instance
        self.observation = observation_instance
        self.logs = logs_instance
        self.gpt = gpt_instance
        

    def run(self):
        '''
        Run the OpenTruth system
        1. get oberservation
        2. laod memory
        3. load dialog
        4. make decision
        5. excute action
        6. update memory
        7. update dialog
        '''
        self.logo()
        self.logs.log_info("Running OpenTruth system")
        while True:
            # 1. get oberservation
            observation = self.observation.get()
            self.logs.log_info(str(observation), "bold green" ,"Observation")
            # 2. laod memory
            memory = self.memory.quer_memory()
            self.logs.log_info(str(memory), "dim cyan", "Memory")
            # 3. load dialog
            dialog = self.dialogManager.read_dialog(config['dialog_path'])
            self.logs.log_info(str(dialog), "dim cyan", "Dialog")
            # 4. make decision
            decision = self.decision.make_decision(observation,memory,dialog)
            self.logs.log_info(str(decision), "dim magenta", "Decision")
            # 5. excute action
            self.action.excute(decision)
            # 6. update memory
            self.memory.updat_memory()
            # 7. update dialog
            self.dialogManager.write_dialog(decision, config['dialog_path'])
            self.logs.log_info(f"current round complete, waiting for {config['interval_time']} seconds for next round")
            print("\n")
            print("\n")
            time.sleep(config['interval_time'])

    def logo(self):
        with open(config["logo_path"]) as f:
            print(f.read())

if __name__ == '__main__':
    gpt_instance = gpt()
    action_instance = actionX()
    decision_instance = decision(gpt_instance)
    dialogManager_instance = dialogManager()
    memory_instance = memory()
    observation_instance = observationX()
    logs_instance = logs()


    openTruth = openTruth(action_instance, decision_instance, dialogManager_instance, memory_instance, observation_instance, logs_instance, gpt_instance)
    openTruth.run()