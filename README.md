# Forge MDK with Mixin and Parchment

这是一个离线包仓库，使用离线包可以大幅降低配置环境时带来的麻烦。离线包的使用方式在最后，前面的部分可以让您对离线包的构成有一个基础的了解。

## 离线包构成

### 下载MDK

[Downloads for Minecraft Forge](https://files.minecraftforge.net/net/minecraftforge/forge/)

右键对应版本的 MDK 复制链接，只截取最后的下载链接，不要复制广告。

下载完毕后先不要打开项目，只打开文件，对MDK进行一些修改。

### 修改Mapping

[Getting Started (parchmentmc.org)](https://parchmentmc.org/docs/getting-started.html)

按照指引将 Mapping 修改为 parchment，这样看到的源码就不会带有参数混淆。

### 添加Mixin

[Minecraft 1.19.2 Forge模组开发 11.Mixin - AcWing](https://www.acwing.com/blog/content/30389/)

这里面说的不全对，实际上首先需要修改 `settings.gradle`

```
pluginManagement {
    repositories {
        gradlePluginPortal()
        maven { url = 'https://maven.minecraftforge.net/' }
        maven { url = 'https://repo.spongepowered.org/maven' }
    }
    resolutionStrategy {
        eachPlugin {
            if (it.requested.id.namespace == 'org.spongepowered') {
                it.useModule('org.spongepowered:mixingradle:0.7-SNAPSHOT')
            }
        }
    }
}
```

只要先把 `settings.gradle` 和 `build.gradle` 改完就行，博客其余的步骤在之后进行。

## 离线包使用

### 准备离线包

本离线包仓库参考 [forge-mdk-offline](https://github.com/mouse0w0/forge-mdk-offline)

`modify.py` 会修改 `settings.gradle` 和 `build.gradle`。如果需要使用 Mixin 和 Parchment（默认为 True），请修改 `modify.py`。如果您需要打开他人的项目，请参考他人的项目配置修改这个文件。

#### Parchment

`CHANGE_MAPPING=True` 即可，需要根据前面的步骤修改 `MAPPING_CHANNEL` 的版本号。

#### Mixin

`ADD_MIXIN=True` 即可，基本上不需要额外修改。

#### Release

在 Github 发布一个新的 Release，Tag 与 Title 都必须与目标 Forge 版本一致，如 `1.19.3-44.1.16`。Release 发布后，Action 会自动进行，请等待约半小时。

记得将仓库的 `Settings->Action->General->Workflow permissions` 设置项设置为 `Read and write permissions` 以避免上传失败。

#### 打开离线包

离线包中有两个文件夹。

- `.gradle` 是离线包的大头，只需要放入 `C:\Users\<用户>`，就可以大幅减少配置文件需要的时间。

- 还有一个是 MDK 文件夹，仅在创建新项目时需要，打开已有项目时可忽略。

现在可以打开项目了，如果按照之前步骤来，应该是第一次打开项目文件夹。打开输出中的 `Gradle for Java`，如果显示失败则关闭 VSCode 重启，直到它显示成功。代理请选择全局，不要屏蔽广告，避免部分资源下载失败。如果使用了离线包，一共需要五到十分钟。

之后在 gradle 的 tasks 里面依次运行

```
forgegradle runs\genVSCodeRuns
forgegradle runs\prepareRunClient
forgegradle runs\prepareRunData
forgegradle runs\prepareRunServer
forgegradle runs\prepareRuns
```

就可以使用 `forgegradle runs\runClient` 运行客户端了，使用 `build\jar` 生成 jar 文件。
