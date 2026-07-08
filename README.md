# AI Narrator Engine · AI 解说视频生成引擎

> 个人开源对标 NarratoAI 的视频解说自动化引擎。

## 核心特性

- **视频理解**：镜头切分（场景 JSON / 抽帧元数据输入）
- **解说文案生成**：按镜头逐段生成，支持剧情解说与带货口播两套模板
- **语音合成**：可插拔 TTS（edge-tts），无环境按时长占位
- **时间轴对齐**：解说词与镜头时间轴自动对齐，输出 SRT + cue 点
- **BGM 匹配规则**：按镜头节奏（快/慢）匹配 BGM 模板规则库

## 快速开始

```bash
python narrator.py --plan examples/plan_demo.json
python narrator.py --plan examples/plan_demo.json --mode sales
```

## 流水线

```
镜头元数据 → 逐镜文案(模板/LLM) → TTS → 时间轴对齐 → SRT+BGM 规则 → outputs/
```

## License

MIT
