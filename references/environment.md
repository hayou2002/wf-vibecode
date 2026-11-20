# wf-vibecode 环境清单

> 由 wf-maker 生成，请勿手改；要改就改 `sources.json` 后重跑 `wf.py env`。

更新时间：2026-11-20

## 技能依赖

| 技能 | 关系 | 来源 | 安装方式 |
| --- | --- | --- | --- |
| arch-grower | 引用 | GitHub Tobi1chi/arch-grower | npx skills add Tobi1chi/arch-grower |
| codex-vibecoding | 引用 | GitHub hayou2002/codex-vibecoding | npx skills add hayou2002/codex-vibecoding |
| git-ship | 引用 | GitHub oil-oil/git-ship | npx skills add oil-oil/git-ship |
| oil-bug-fix | 引用 | GitHub oil-oil/oil-dev-skills › skills/oil-bug-fix | npx skills add oil-oil/oil-dev-skills --skill oil-bug-fix |
| oil-code-review | 引用 | GitHub oil-oil/oil-dev-skills › skills/oil-code-review | npx skills add oil-oil/oil-dev-skills --skill oil-code-review |
| oil-delegate | 引用 | GitHub oil-oil/oil-dev-skills › skills/oil-delegate | npx skills add oil-oil/oil-dev-skills --skill oil-delegate |
| oil-explore | 引用 | GitHub oil-oil/oil-dev-skills › skills/oil-explore | npx skills add oil-oil/oil-dev-skills --skill oil-explore |
| oil-frontend | 引用 | GitHub oil-oil/oil-frontend | npx skills add oil-oil/oil-frontend |
| oil-govern | 引用 | GitHub oil-oil/oil-dev-skills › skills/oil-govern | npx skills add oil-oil/oil-dev-skills --skill oil-govern |
| oil-plan | 引用 | GitHub oil-oil/oil-dev-skills › skills/oil-plan | npx skills add oil-oil/oil-dev-skills --skill oil-plan |
| project-map | 引用 | 本机目录 | 随本机技能目录同步（无上游仓库） |
| vibehub | 引用 | GitHub oil-oil/vibe-hub-skill › skills/vibehub | npx skills add oil-oil/vibe-hub-skill --skill vibehub |
| webapp-testing | 引用 | GitHub anthropics/skills › skills/webapp-testing | npx skills add anthropics/skills --skill webapp-testing |
| wf-design | 引用 | GitHub hayou2002/wf-design | npx skills add hayou2002/wf-design |
| wf-github-ops | 引用 | GitHub hayou2002/wf-github-ops | npx skills add hayou2002/wf-github-ops |

## 自定义配置

第一次用到下面这些技能或工作流时,先问用户一次,再把结果记到对应位置;不改技能文件,不记密钥值。

| 技能 | 需要你定的事 | 记在哪 | 状态 |
| --- | --- | --- | --- |
| oil-delegate | 委派给哪个 CLI、各用途交给谁 | ~/.oil-dev/preferences.md | 待配置 |

## 凭据与配置

本清单不记录任何密钥值。需要你自行准备的项目：

- 暂无登记；如果用到了需要密钥的步骤，用 `wf.py link <工作流> <技能> --credentials "需要什么、放在哪"` 补上。

## 恢复步骤

1. 按上表逐项安装或确认技能已就位。
2. 用 `wf.py check <工作流>` 核对每个技能的版本是否和登记时一致。
3. 按「自定义配置」逐项确认；待配置的先问用户，不要替用户选。
4. 凭据按「凭据与配置」一节自行准备，不要写进本目录。
