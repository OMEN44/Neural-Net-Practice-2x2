def render_loop(objects, surface):
    try:
        for entity in objects:

            try:
                entity.update()
            except Exception as e:
                print(e)
                entity.update()
            surface.blit(entity.surf, entity.rect.topleft)
    except TypeError:
        for entity in objects.getList():

            try:
                entity.update()
            except Exception as e:
                print(e)
                entity.update()
            surface.blit(entity.surf, entity.rect.topleft)
