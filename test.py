row1 = 0
row2 = 1
col1 = 0
col2 = 1
link_groups = {}


def link_boxes(row1, col1, row2, col2):
    box1 = row1,col1
    box2 = row2,col2
    group1 = link_groups.get(box1, [box1])
    group2 = link_groups.get(box2, [box2])
    group = group1+group2

    for i in group:
        link_groups[i] = group
    
    
    



    print(f"Linked boxes at {box1} and {box2}")

link_boxes(row1, col1, row2, col2)
print(link_groups)

link_boxes(0,0,5,5)
print(link_groups)

link_boxes(2,2,7,7)
print(link_groups)