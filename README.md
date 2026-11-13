# wf-vibecode

把「我想做个东西」变成在你自己机器上真的能跑、能验收的改动。

一句话原则:**能做小的就不做大,做完必须有能验证的证据。**

## 怎么走

**底座(每趟都走)**:摸现场 → 定档与边界 → 先找可复用的 → 逐片实现 → 验证说真话 → 收口交付

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

## 安装

```bash
npx skills add hayou2002/wf-vibecode
```

## 依赖

`codex-vibecoding`(分档、复用、证据这些细则的来源)、`oil-explore`、`oil-plan`、`oil-frontend`、`oil-code-review`、`oil-govern`、`git-ship`,以及同系列的 `wf-github-ops`、`wf-design`。按车道取用,不必全装。

## 同系列

- [wf-maker](https://github.com/hayou2002/wf-maker):把流程做成工作流 Skill
- [wf-github-ops](https://github.com/hayou2002/wf-github-ops):本地 Git 整理与 GitHub 上传
- [wf-design](https://github.com/hayou2002/wf-design):网页、演示、图片、正式文件

## 许可

MIT
