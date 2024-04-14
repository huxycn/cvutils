import cvutils


img_path = 'obs://bigdata-tmp/temporary_upload/test/1674011760049056000-1692_719625000.png'

# img_path = '/home/huxiaoyang/Downloads/1674011760049056000-1692_719625000.png'

json_path = cvutils.iopath.with_tag_suffix(img_path, tag='@lm-dino-20220903-cc3b046', suffix='.json')

img = cvutils.iopath.load(img_path)
json_obj = cvutils.iopath.load(json_path)

for ann in json_obj['annotations']:
    cat_name = ann['category_name']
    bbox = ann['bbox']
    conf = ann['confidence']

    cvutils.vis.draw_bbox2d(img, bbox, (0, 0, 255), label=f'{cat_name[:3]}:{conf:.2f}')

cvutils.vis.imshow(img)
