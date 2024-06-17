CHANGE_MAPPING = True
MAPPING_REPO = "        maven { url = 'https://maven.parchmentmc.org' }\n"
MAPPING_PLUGIN = "    id 'org.parchmentmc.librarian.forgegradle' version '1.+'\n"
# GET VERSION HERE: https://parchmentmc.org/docs/getting-started
MAPPING_CHANNEL = "    mappings channel: 'parchment', version: '2023.09.03-1.20.1'\n"

ADD_MIXIN = True
MIXIN_REPO = "        maven { url = 'https://repo.spongepowered.org/maven' }\n"
MIXIN_STRATEGY = """    resolutionStrategy {
        eachPlugin {
            if (it.requested.id.namespace == 'org.spongepowered') {
                it.useModule('org.spongepowered:mixingradle:0.7.+')
            }
        }
    }
"""
MIXIN_PLUGIN = "    id 'org.spongepowered.mixin' version '0.7.+'\n"
MIXIN_SRC = """mixin {
    add sourceSets.main, "modid.refmap.json"
}
"""
MIXIN_NAME = ""
MIXIN_ARG = "            arg '-mixin.config=modid.mixins.json'\n"
MIXIN_PROCESSOR = "    annotationProcessor 'org.spongepowered:mixin:0.8.5:processor'\n"
MIXIN_CONFIG = '                "MixinConfigs": "modid.mixins.json"\n'

fbuildin = open("build/build.gradle", "r")
fbuildout = open("build/buildnew.gradle", "w")

lines = fbuildin.readlines()
for line in lines:
    lineraw = line.replace("\n", "").lstrip(" ")

    if ADD_MIXIN and lineraw.find("Implementation-Timestamp") != -1:
        line = line.replace("\n", "") + ",\n"

    if CHANGE_MAPPING and lineraw.find("mappings channel") == 0:
        fbuildout.write(MAPPING_CHANNEL)
    else:
        fbuildout.write(line)

    if lineraw.find("net.minecraftforge.gradle") != -1:
        if CHANGE_MAPPING:
            fbuildout.write(MAPPING_PLUGIN)
        if ADD_MIXIN:
            fbuildout.write(MIXIN_PLUGIN)
    
    if ADD_MIXIN and lineraw.find("println") == 0:
        fbuildout.write(MIXIN_SRC)

    if ADD_MIXIN and lineraw.find("enabledGameTestNamespaces") != -1:
        fbuildout.write(MIXIN_ARG)

    if ADD_MIXIN and lineraw.find("net.minecraftforge:forge") != -1:
        fbuildout.write(MIXIN_PROCESSOR)

    if ADD_MIXIN and lineraw.find("Implementation-Timestamp") != -1:
        fbuildout.write(MIXIN_CONFIG)


fbuildin.close()
fbuildout.close()

fsetin = open("build/settings.gradle", "r")
fsetout = open("build/settingsnew.gradle", "w")
flag = 0

lines = fsetin.readlines()
for line in lines:
    lineraw = line.replace("\n", "").lstrip(" ")
    fsetout.write(line)

    if lineraw.find("maven") == 0:
        if CHANGE_MAPPING:
            fsetout.write(MAPPING_REPO)
        if ADD_MIXIN:
            fsetout.write(MIXIN_REPO)
            flag = 2

    flag -= 1
    if ADD_MIXIN and flag == 0:
        fsetout.write(MIXIN_STRATEGY)

fsetin.close()
fsetout.close()
