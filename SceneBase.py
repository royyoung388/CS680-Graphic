from Component import Component
from Light import Light


class SceneBase:
    shaderProg = None

    lights = None

    def toggle_light(self, index):
        if not self.lights:
            return

        index -= 1
        # out of index
        if index < 0 or index >= len(self.lights):
            return

        self.lights[index].toggleLight()
        self.shaderProg.setLight(index, self.lights[index])
