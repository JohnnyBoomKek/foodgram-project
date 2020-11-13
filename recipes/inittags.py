from recipes.models import Tag

tags = ['B', 'L', 'D']
for tag in tags:
    new_tag = Tag(tag_name=tag)
    new_tag.save()