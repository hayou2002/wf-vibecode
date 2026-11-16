# wf-vibecode

![wf-vibecode 工作流示意:需求先翻准,按风险分三档,做完给证据](assets/readme/hero.svg)

把「我想做个东西」变成在你自己机器上真的能跑、能验收的改动。

一句话原则:**能做小的就不做大,做完必须有能验证的证据。**

## 怎么走

**底座(默认全走,按车道裁剪)**:需求翻译 → 摸现场(看代码 + 访问用户) → 定档与边界 → 先找可复用的 → 逐片实现 → 验证说真话 → 收口交付

**车道(选一条)**:

| 车道 | 什么时候走 |
| --- | --- |
| 1 小改直通(T0) | 文案、样式、改法明确的小缺陷 |
| 2 单点功能(T1) | 一个用户能感觉到的功能,边界清楚 |
| 3 全流程(T2) | 新产品、多层改动、登录、数据迁移、外部集成 |
| 4 故障修复 | 有明确报错或行为不对 |
| 5 已有产物收口 | 实现已完成,只要打包、上传、推送 |
| 6 收尾治理 | 文档、测试、worktree 乱了 |

拿不准先按 2 走;做起来发现跨了多层、动了数据或权限,再升到 3。降档不等于跳过安全与回归检查。

需求说不清的话,先把它翻成「准话」再动手;现场摸不全,就访问你一轮,只问代码里查不到的。

过程中它会顺手做两件记录:用到的术语记进项目的 `docs/术语表.md`(词条 + 对应功能),需求背景写进项目 `AGENTS.md`——以后新会话和别的 AI 能一眼接上。

- 故障修复先复现、再找根因，用 `oil-bug-fix`；原因和改法已经明确的，按 T0 直接修。
- 验证分三层：编码途中只跑秒级检查，写完跑关联快测，全量测试与构建留到合并前一次跑完。

## 三条刹车

- 只在缺的信息会改变用户能看见的行为、数据安全、认证、付费或对外副作用时才问,一次问完。
- 破坏性动作先问:删数据、改表结构、覆盖别人正在改的文件、强推、改线上配置。
- **改代码不等于允许 push、部署、发布、花钱。** 用户明确点名了才做。

## 验证不靠嘴说

```bash
py -3 scripts/run_checks.py            # 只列出这个项目该跑什么检查
py -3 scripts/run_checks.py --yes      # 确认后执行,逐项记录命令、退出码、耗时、输出尾部
```

它从项目里认出测试、lint、类型检查和构建命令(`package.json`、pytest、Cargo、Go、Makefile,以及 `AGENTS.md` 里写的命令)。程序没装会标「跑不了」,不算失败。

跑完给一行结论:通过、命中还是跑不动,括号里都写着原因,不用记编号。

web 界面类改动可以挂 `webapp-testing`,用真实浏览器把关键路径点一遍。

## 安装

```bash
npx skills add hayou2002/wf-vibecode
```

## 依赖

故障修复另需 `oil-bug-fix`（与 `oil-*` 同一仓库）；委派是可选项，Codex 内先用原生子 Agent。

`codex-vibecoding`(分档、复用、证据这些细则的来源)、`vibehub`(把口语需求翻准)、`oil-explore`、`oil-plan`、`oil-frontend`、`oil-code-review`、`oil-govern`、`oil-delegate`、`git-ship`,以及同系列的 `wf-github-ops`、`wf-design`;`webapp-testing`(可选,web 界面真浏览器验证)。按车道取用,不必全装。

## 同系列

- [wf-maker](https://github.com/hayou2002/wf-maker):把流程做成工作流 Skill
- [wf-github-ops](https://github.com/hayou2002/wf-github-ops):本地 Git 整理与 GitHub 上传
- [wf-design](https://github.com/hayou2002/wf-design):网页、演示、图片、正式文件

## 许可

MIT
