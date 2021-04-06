import os
results = [b'610,519,211,128,120,0.4172363281,0.0289306641,-0.0058593750\n', b'625,337,182,122,109,0.5660400391,-0.0078125000,0.1707763672\n', b'618,460,216,137,133,0.4370117188,0.6450195312,-0.3570556641\n', b'578,327,174,110,107,0.4483642578,-0.0078125000,0.0791015625\n', b'548,493,211,127,114,0.4794921875,-0.0489501953,0.1654052734\n', b'600,492,219,151,138,0.8477783203,0.3051757812,0.0804443359\n', b'542,274,166,123,113,0.8676757812,0.2126464844,0.1915283203\n', b'637,493,213,132,121,0.4014892578,0.1207275391,-0.1138916016\n', b'619,517,222,134,126,0.4422607422,-0.1582031250,0.4594726562\n', b'642,524,227,140,131,0.3979492188,-0.1563720703,0.6297607422\n', b'615,414,205,134,131,0.4776611328,-0.1474609375,0.4476318359\n', b'547,521,215,147,137,0.5187988281,-0.1219482422,0.4617919922\n', b'518,270,157,120,110,0.5426025391,-0.1179199219,0.6051025391\n', b'617,303,177,138,127,0.5864257812,-0.1068115234,0.5577392578\n', b'619,334,186,125,114,0.5555419922,-0.1134033203,0.4984130859\n', b'600,510,211,141,128,0.4211425781,-0.1474609375,0.4617919922\n', b'628,510,217,128,123,0.4632568359,-0.1573486328,0.6002197266\n', b'589,276,166,108,104,0.5843505859,-0.1104736328,0.6241455078\n', b'569,313,172,117,111,0.6549072266,-0.0673828125,0.5045166016\n', b'643,300,177,120,115,0.6341552734,-0.0610351562,0.5780029297\n', b'634,325,182,122,116,0.6234130859,-0.0859375000,0.5684814453\n', b'627,447,194,125,110,0.3923339844,-0.1140136719,0.3018798828\n', b'618,509,217,149,132,0.9932861328,0.5537109375,0.1311035156\n', b'603,404,183,125,114,0.6156005859,-0.0140380859,0.2384033203\n', b'523,536,206,142,129,0.4508056641,-0.1441650391,0.3812255859\n', b'525,518,201,137,123,0.5328369141,-0.1279296875,0.4365234375\n']

letters = 'ZOQMDGJPUKFBSYNRLIEATCHXWV'
name = "Stelios"
for i,letter in enumerate(letters):
    data_path = os.path.join(os.path.dirname(__file__), 'data', '{}'.format(letter))
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    with open(os.path.join(os.path.dirname(__file__), 'data', '{}'.format(letter), '{}.csv'.format(name.replace(' ','_'))), 'a', 777) as f:
        f.write(results[i].decode('utf-8'))

