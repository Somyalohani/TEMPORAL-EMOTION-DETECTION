#!/usr/bin/env python


import asyncio
import websockets
import json

#Global
FRAMES = [] 

async def consumer(websocket, path):
    async for message in websocket:
        result = ""
        FRAMES.append(message)
        n = len(FRAMES)
        if(n >= 30):
            rdata = FRAMES[n-30:n]
            lis0 = []
            lis1 = []
            lis2 = []
            lis3 = []
            lis4 = []
            lis5 = []
            for dic in rdata:
                try:
                    dicti = eval(dic)
                    lis0.append(dicti['emotions']['anger'])
                    lis1.append(dicti['emotions']['disgust'])
                    lis2.append(dicti['emotions']['fear'])
                    lis3.append(dicti['emotions']['joy'])
                    lis4.append(dicti['emotions']['sadness'])
                    lis5.append(dicti['emotions']['surprise'])
                except:
                    SyntaxError
            l0 = 0
            l1 = 0
            l2 = 0
            l3 = 0
            l4 = 0
            l5 = 0
            l6 = 0
            for i in range(30):
                a = max([lis0[i], lis1[i], lis2[i], lis3[i], lis4[i], lis5[i]])
                if (a < 0.01):
                    l6 += 1
                    l0 += -1
                    l1 += -1
                    l2 += -1
                    l3 += -1
                    l4 += -1
                    l5 += -1
                elif (lis0[i] == a):
                    l0 += 1
                    l1 += -1
                    l2 += -1
                    l3 += -1
                    l4 += -1
                    l5 += -1
                    l6 += -1
                elif (lis1[i] == a):
                    l0 += -1
                    l1 += 1
                    l2 += -1
                    l3 += -1
                    l4 += -1
                    l5 += -1
                    l6 += -1
                elif (lis2[i] == a):
                    l0 += -1
                    l1 += -1
                    l2 += 1
                    l3 += -1
                    l4 += -1
                    l5 += -1
                    l6 += -1
                elif (lis3[i] == a):
                    l0 += -1
                    l1 += -1
                    l2 += -1
                    l3 += 1
                    l4 += -1
                    l5 += -1
                    l6 += -1
                elif (lis4[i] == a):
                    l0 += -1
                    l1 += -1
                    l2 += -1
                    l3 += -1
                    l4 += 1
                    l5 += -1
                    l6 += -1
                elif (lis5[i] == a):
                    l0 += -1
                    l1 += -1
                    l2 += -1
                    l3 += -1
                    l4 += -1
                    l5 += 1
                    l6 += -1
                a = max([l0, l1, l2, l3, l4, l5, l6])
                if (l6 == a):
                    result = "Neutral"
                elif (l0 == a):
                    result = "Angry"
                elif (l1 == a):
                    result = "Disgusted"
                elif (l2 == a):
                    result = "Fearful"
                elif (l3 == a):
                    result = "Happy"
                elif (l4 == a):
                    result = "Sad"
                elif (l5 == a):
                    result = "Surprised"
                
                
        message1 = "Result of emotion detection based on maximum confidence: " + result
        print(message)
        print(message1)
        await websocket.send(result)



if __name__ == '__main__':
    start_server = websockets.serve(consumer, "localhost", 3000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
