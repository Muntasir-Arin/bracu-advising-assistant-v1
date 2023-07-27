import json
import itertools
from PIL import Image, ImageDraw, ImageFont
#calculation algorithm


def day_calc(arr):
    new_arr = sorted(arr)
    total = 0
    for i in range(len(new_arr)-1):
        f= (new_arr[i+1]-new_arr[i])*2
        if f ==0:
            total+= 100000
            break
        else:
            total+= f
    return total   

def week_calc(dict):
    total = 0
    for i in dict.values():
        total+= day_calc(i)+7
    return total 
         
def week_main(arr):
    dict1= {}
    for i in arr:
        if i//100000!= 0 :
            if 6 not in dict1:
                dict1[6]=[]
            dict1[6]+= [i//100000]
        elif i//10000!= 0 :
            if 5 not in dict1:
                dict1[5]=[]
            dict1[5]+= [i//10000]
        elif i//1000!= 0 :
            if 4 not in dict1:
                dict1[4]=[]
            dict1[4]+= [i//1000]
        elif i//100!= 0 :
            if 3 not in dict1:
                dict1[3]=[]
            dict1[3]+= [i//100]
        elif i//10!= 0 :
            if 2 not in dict1:
                dict1[2]=[]
            dict1[2]+= [i//10]
        else :
            if 1 not in dict1:
                dict1[1]=[]
            dict1[1]+= [i]
    
    return week_calc(dict1)


#functions

def convert_to_int(input_string):
    day_dict = {'Sa': 1, 'Su': 10, 'Mo': 100, 'Tu': 1000, 'We': 10000, 'Th': 100000}
    num_dict = {'08': 1, '09': 2, '11': 3, '12': 4, '02': 5, '03': 6, '05': 7}
    day = input_string[:2]
    num = input_string[2:]
    if day in day_dict and num in num_dict:
        return day_dict[day] * num_dict[num]
    
def course_covert_ONE(data):
    course = {}
    for i in data:
        k= i[2].split()
        for j in range(len(k)):
            if j%3==0:
                if (int(i[1][:2])-1) not in course:
                    course[(int(i[1][:2])-1)]=[]
                course[(int(i[1][:2])-1)] += [convert_to_int(k[j][0:2]+ k[j][3:5])]
    return course

def course_covert_ONE_online(data):
    course = {}
    for i in data:
        if int(i[3])<= 0:
            continue
        k= i[2].split()
        for j in range(len(k)):
            if j%3==0:
                if (int(i[1][:2])-1) not in course:
                    course[(int(i[1][:2])-1)]=[]
                course[(int(i[1][:2])-1)] += [convert_to_int(k[j][0:2]+ k[j][3:5])]
    return course
        
def course_covert_MANY(courses, available):
    #accessing data
    f = open('data.json')
    data = json.load(f)
    f.close()
    #--------------
    all_courses = {}
    if available:
        for i in courses:
            all_courses[i.upper()]= course_covert_ONE_online(data[i.upper()])
    else:
        for i in courses:
            all_courses[i.upper()]= course_covert_ONE(data[i.upper()])
        
 
    return all_courses
        
def find_best(courselist, filter, available, top):
    a = course_covert_MANY(courselist, available)
    if filter:
        del_list= []
        for key, value in filter.items():
            if key.upper() in a:
                for p,l in a[key.upper()].items():
                    if (p+1) not in value:
                        del_list.append((key.upper(),p))
        
        for s,d in del_list:
            del a[s][d] 
    
    list1=[]
    for k, v in a.items():
        list1.append(list(v.keys()))
        
    z=list(itertools.product(*list1))
    test_dict={}
    for i in z :
        day = []
        for j in range(len(i)) :
            day+= a[courselist[j].upper()][i[j]]
        
        val= week_main(day)
        if val<100000:
            test_dict[i] = val 
        
    sorted_list = sorted(test_dict.items(), key=lambda x:x[1] )
    
    return a, sorted_list[:top]


def draw_routine_ONE(data_list, input_image_path, output_image_path):
    # Define grid properties
    margin = 180
    grid_columns = 6
    grid_rows = 7

    # Open the input image
    image = Image.open(input_image_path)
    image_width, image_height = image.size

    # Calculate grid cell dimensions
    cell_width = 1+ (image_width - (2 * margin)) // grid_columns
    cell_height = (image_height - (2 * margin)) // grid_rows

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Load a font to write the text
    font_path = "Roboto-Regular.ttf"  # Replace with the actual font file path
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)

    # Iterate over the data list and draw each text on the image
    for data in data_list:
        location, text = data

        # Calculate the target cell based on the provided location
        column = len(location)-1
        row = int(location[0])-1

        # Calculate the coordinates of the cell's top-left corner
        x = 273 + (column * cell_width)
        y = 315 + (row * cell_height)

        # Write the text on the image at the calculated position
        draw.text((x, y), text, font=font, fill="#A6E6F7")

    # Save the modified image
    image.save(output_image_path)

def main_function(courselist, filter=None, available=False, top=5):
    a, base = find_best(courselist, filter, available, top)
    main_list =[]
    for z in base:
        listz= []
        b= z[0]
        for i in range(len(b)):
            k = a[courselist[i].upper()][b[i]]
            for kk in k:
                listz.append([str(kk) , courselist[i]+" ("+str(b[i]+1)+")" ])
        main_list.append(listz)
    count= 1        
    for i in main_list:
        output= "output/Best "+str(count)+".png"
        draw_routine_ONE(i, "1.png", output)
        count+=1
    

def course_suggest (courses, filter=None, available=False, course_num=5,lab=2 ,top=5, must=False):
    labs= {'CSE111', 'CSE350', 'CSE220', 'CSE472', 'CSE427', 'CSE360', 'CSE484', 'CSE446', 'ARC101', 'CSE330', 'CSE424', 'ARC401', 'PHY112', 'CSE422', 'MAT092', 'CSE221', 'ARC201', 'ARC402', 'ARC102', 'CSE370', 'CSE460', 'CSE428', 'EEE421', 'PHY111', 'ARC503', 'EEE308', 'ARC501', 'EEE447', 'ARC301', 'CSE341', 'CSE420', 'CSE421', 'CSE489', 'EEE431', 'ARC502', 'CSE321', 'ARC302', 'CSE391', 'EEE472', 'CSE461', 'CSE251', 'CSE447', 'ECE103', 'EEE103', 'CSE471', 'CSE260', 'MAT091', 'ARC202', 'MAT120', 'CSE110', 'EEE385', 'CSE101', 'CSE250', 'CSE423', 'ECE447', 'CSE490', 'CSE310'}
    courses= list(map(str.upper, courses))
    if must:
        must= list(map(str.upper, must))
        for i in must:
            courses.remove(i)
    if must:
        all_combination = itertools.combinations(courses, course_num-len(must))
    else:
        all_combination = itertools.combinations(courses, course_num)
    a={}
    u_base=[]
    for i in all_combination:
        if must:
            i= tuple(list(i)+must)
        if len(labs.intersection(set(list(i))))<lab:
            continue
        a1, base1 = find_best(list(i), filter, available, top)
        a.update(a1)
        for j in base1:
            u_base.append((j[0],j[1], list(i)))
    base= sorted(u_base, key=lambda x: x[1])
    main_list =[]
    for z in base:
        courselist= z[2]
        listz= []
        b= z[0]
        for i in range(len(b)):
            k = a[courselist[i].upper()][b[i]]
            for kk in k:
                listz.append([str(kk) , courselist[i]+" ("+str(b[i]+1)+")" ])
        main_list.append(listz)
    count= 1     
    for i in main_list:
        output= "output/Best "+str(count)+".png"
        draw_routine_ONE(i, "1.png", output)
        count+=1
        if count>top:
            break


