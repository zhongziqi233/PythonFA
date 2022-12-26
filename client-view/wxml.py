import xml.dom.minidom

x0_arr = [1, 1, 1, 1]
y0_arr = [2, 2, 2, 2]
x1_arr = [3, 3, 3, 3]
y1_arr = [4, 4, 4, 4]
name_arr = ['a', 'b', 'c']

if len(x0_arr) > 0:
    mainDom = xml.dom.minidom.getDOMImplementation().createDocument(None, 'annotation', None)
    root = mainDom.documentElement
    for i in range(len(x0_arr)):
        obj = mainDom.createElement('object')
        root.appendChild(obj)
        print(i)

        if len(name_arr) - 1 < i:
            name = 'unname' + str(len(name_arr) - 1 - i)
        else:
            name = name_arr[i]
        nameE = mainDom.createElement('name')
        nameT = mainDom.createTextNode(name)
        nameE.appendChild(nameT)
        obj.appendChild(nameE)
        print(i)

        bndbox = mainDom.createElement('bndbox')
        obj.appendChild(bndbox)
        print(i)

        Ex0 = mainDom.createElement('xmin')
        Tx0 = mainDom.createTextNode(str(x0_arr[i]))
        Ex0.appendChild(Tx0)
        bndbox.appendChild(Ex0)
        print(i)

        Ey0 = mainDom.createElement('ymin')
        Ty0 = mainDom.createTextNode(str(y0_arr[i]))
        Ey0.appendChild(Ty0)
        bndbox.appendChild(Ey0)
        print(i)

        Ex1 = mainDom.createElement('xmax')
        Tx1 = mainDom.createTextNode(str(x1_arr[i]))
        Ex1.appendChild(Tx1)
        bndbox.appendChild(Ex1)
        print(i)

        Ey1 = mainDom.createElement('ymax')
        Ty1 = mainDom.createTextNode(str(y1_arr[i]))
        Ey1.appendChild(Ty1)
        bndbox.appendChild(Ey1)
        print(i)

    with open('annotation.xml', 'w') as fs:
        mainDom.writexml(fs, addindent='    ', newl='\n')
        fs.close()