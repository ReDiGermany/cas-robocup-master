import asyncio
import sys
import threading
import jsonpickle
import websockets

from src import Singleton,CASENV

from src.imageDetection import runDetection

print("Welcome")

s1 = Singleton()
    
async def establishConnection():
    WS_PORT = CASENV.WS_PORT
    WS_AUTH = CASENV.WS_AUTH
    
    WS_HOST = "192.168.171.136"
    if(len(sys.argv)>1):
        WS_HOST = sys.argv[1]

    uri = f"ws://{WS_HOST}:{WS_PORT}"

    authed = False

    print(f"Connecting to {uri}")
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print(f"Connected to {uri}")
                await websocket.send(jsonpickle.encode({"type":"auth","token":WS_AUTH},unpicklable=False))
                # print(jsonpickle.encode(websocket,unpicklable=False))
                while websocket.close_rcvd==None:
                    message = await websocket.recv()
                    json = jsonpickle.decode(message)
                    if "type" in json:
                        if json["type"]=="authenticated":
                            authed = True
                            print("Authenticated")

                    if authed:
                        while(True):
                            await websocket.send(jsonpickle.encode({"type":"data","data":s1.data},unpicklable=False))
                            await asyncio.sleep(1/10)
                            #print(f"message={message}")
        except:
            pass
    print("done?")
        

if __name__ == "__main__":
    detect = threading.Thread(target=runDetection, daemon=True)
    detect.start()
    asyncio.run(establishConnection())
   
# # https://im-coder.com/wie-berechne-ich-den-schnittpunkt-zweier-linien-in-python.html
# def line_intersection(line1, line2):
#     xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
#     ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

#     def det(a, b):
#         return a[0] * b[1] - a[1] * b[0]

#     div = det(xdiff, ydiff)
#     if div == 0:
#         raise Exception('lines do not intersect')

#     d = (det(*line1), det(*line2))
#     x = det(d, xdiff) / div
#     y = det(d, ydiff) / div
#     return x, y

# width = 640
# height = 480

# top_left = (125,175)
# top_right = (width-140,175)
# bottom_left = (-30,height-120)
# bottom_right = (width+5,height-120)

# def loadData():
#     global top_left
#     global top_right
#     global bottom_right
#     global bottom_left
#     f = open("field", "r")
#     data = f.read().splitlines()
#     top_left = (int(data[0].split("x")[0].split(".")[0]),int(data[0].split("x")[1].split('.')[0]))
#     top_right = (int(data[1].split("x")[0].split(".")[0]),int(data[1].split("x")[1].split('.')[0]))
#     bottom_right = (int(data[2].split("x")[0].split(".")[0]),int(data[2].split("x")[1].split('.')[0]))
#     bottom_left = (int(data[3].split("x")[0].split(".")[0]),int(data[3].split("x")[1].split('.')[0]))
#     # print(data)

# print("Loading Config")
# loadData()
# print("Config Loaded")

# print("Loading model")
# model = YOLO('./best_m.pt')  # load an official detection model
# print("Model loaded")

# results = model(source=0, stream=True,verbose=False) 

# now = datetime.now()
# time = now.second
# fps = 0

# for result in results:
#     now = datetime.now()
#     currtime = now.second
#     if currtime != time:
#         print(f"FPS = {fps}")
#         time = currtime
#         fps = 0
#     else:
#         fps = fps + 1 

#     boxes = result.boxes  # Boxes object for bbox outputs

#     im = Image.fromarray(result.orig_img[...,::-1].copy())
#     img1 = ImageDraw.Draw(im)
#     img1.line([top_left,top_right], width=5, fill="#ffffff")
#     img1.line([top_left,bottom_left], width=5, fill="#ffffff")
#     img1.line([top_right,bottom_right], width=5, fill="#ffffff")
#     img1.line([bottom_left,bottom_right], width=5, fill="#ffffff")

#     # s1.resetBalls()
#     balls = []
#     robots = []

#     for idx,c in enumerate(result.boxes.cls):
#         if result.names[int(c)] == "robot" or result.names[int(c)]=="ball":
#             w, h = 220, 190
#             shape = [(boxes.xyxy[idx][0], boxes.xyxy[idx][1]), (boxes.xyxy[idx][2],boxes.xyxy[idx][3])]
#             position_x = boxes.xyxy[idx][0] + ((boxes.xyxy[idx][2] - boxes.xyxy[idx][0]) / 2)
#             position_y = boxes.xyxy[idx][3]
#             left_intersection = line_intersection((top_left,bottom_left),((0,position_y),(position_x,position_y)))
#             right_intersection = line_intersection((top_right,bottom_right),((width,position_y),(position_x,position_y)))
#             bottom_intersection = line_intersection((bottom_left,bottom_right),((position_x,position_y),(position_x,bottom_left[1])))
#             top_intersection = line_intersection((top_left,top_right),((position_x,position_y),(position_x,top_left[1])))
            
#             # if left_intersection:
#             #     img1.rectangle([
#             #         (left_intersection[0],position_y-1),
#             #         (position_x+1,position_y+1)
#             #     ], fill ="blue")
#             # else:
#             #     img1.rectangle([
#             #         (0,position_y-1),
#             #         (position_x+1,position_y+1)
#             #     ], fill ="blue")

#             # if bottom_intersection:
#             #     img1.rectangle([
#             #         (position_x,position_y),
#             #         (position_x+1,bottom_intersection[1]+1)
#             #     ], fill ="blue")
#             # else:
#             #     img1.rectangle([
#             #         (position_x,position_y),
#             #         (position_x+1,height)
#             #     ], fill ="blue")
            
#             if left_intersection and bottom_intersection and right_intersection and top_intersection:
#                 x_percent = int(((position_x - left_intersection[0]) / (right_intersection[0] - left_intersection[0])) * 100)/100
#                 y_percent = int(((position_y - bottom_intersection[1]) / (top_intersection[1] - bottom_intersection[1])) * 100)/100

#                 if result.names[int(c)]=="ball":
#                     balls.append({"x":x_percent,"y":y_percent})

#                 if result.names[int(c)]=="robot":
#                     robots.append({
#                         "x": x_percent,
#                         "y": y_percent,
#                         "id": "blue",
#                         "team": "blue",
#                         "angle": 0,
#                     })

#                 outline = "red"
#                 inArea = x_percent>0 and x_percent<1 and y_percent>0 and y_percent<1
#                 if inArea:
#                     outline = "#4ae53a"

#                 # img1.rectangle(shape, outline = outline, width=2)
#                 if inArea:
#                     img1.text((position_x-1,boxes.xyxy[idx][1]-20-1), fill ="#000000", outline="#000", text=f"x = {x_percent} | y = {y_percent} | label = {result.names[int(c)]}")
#                     img1.text((position_x-1,boxes.xyxy[idx][1]-20+1), fill ="#000000", outline="#000", text=f"x = {x_percent} | y = {y_percent} | label = {result.names[int(c)]}")
#                     img1.text((position_x+1,boxes.xyxy[idx][1]-20-1), fill ="#000000", outline="#000", text=f"x = {x_percent} | y = {y_percent} | label = {result.names[int(c)]}")
#                     img1.text((position_x+1,boxes.xyxy[idx][1]-20+1), fill ="#000000", outline="#000", text=f"x = {x_percent} | y = {y_percent} | label = {result.names[int(c)]}")
#                     img1.text((position_x,boxes.xyxy[idx][1]-20), fill ="#ffffff", outline="#000", text=f"x = {x_percent} | y = {y_percent} | label = {result.names[int(c)]}")
#         # else:
#             # print(result.names[int(c)])
#     s1.setBalls(balls)
#     s1.setRobots(robots)

    
#     open_cv_image = np.array(im.convert("RGB")) 

#     scale_percent = 200
#     width = int(open_cv_image.shape[1] * scale_percent / 100)
#     height = int(open_cv_image.shape[0] * scale_percent / 100)
#     dim = (width, height)
    
#     resized = cv.resize(open_cv_image, dim, interpolation = cv.INTER_AREA)
#     final = cv.cvtColor(resized, cv.COLOR_BGR2RGB)

#     cv.imshow('img',final)



