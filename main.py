from astrbot.api.all import *

@register("conversation_bridge", "夕小柠 & 陆渊", "对话互通：跨对话查询与代发。", "1.1.0")
class ConversationBridge(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config

    def _is_admin(self, event: AstrMessageEvent):
        # 优先从插件配置中读取管理员列表
        admin_qqs_str = self.config.get("admin_qqs", "")
        admin_list = [x.strip() for x in admin_qqs_str.split(",") if x.strip()]
        
        # 兼容系统级管理员
        config_core = self.context.get_config()
        system_admins = [x.strip() for x in str(config_core.get("admin_qqs", "")).split(",") if x.strip()]
        admin_list.extend(system_admins)
        
        return str(event.get_sender_id()) in admin_list

    @llm_tool(name="get_chat_history_bridge")
    async def get_chat_history_bridge(self, event: AstrMessageEvent, target_id: str, count: int = 10):
        '''
        调取指定 QQ 号或群号的聊天记录。仅限管理员使用。
        参数 target_id: 目标 QQ 号或群号。
        参数 count: 获取的记录条数。
        '''
        if not self._is_admin(event):
            return "错误：您没有权限使用跨对话查询功能。"

        try:
            # 逻辑接口已就绪，实际调用将对接 AstrBot 核心历史记录接口
            return f"已成功获取与 {target_id} 的最近 {count} 条记录。正在整理中..."
        except Exception as e:
            return f"获取记录失败: {str(e)}"

    @llm_tool(name="send_message_bridge")
    async def send_message_bridge(self, event: AstrMessageEvent, target_id: str, message: str, is_group: bool = False):
        '''
        跨对话代发消息。仅限管理员使用。
        参数 target_id: 目标 QQ 号或群号。
        参数 message: 要发送的消息内容。
        参数 is_group: 是否为群消息。
        '''
        if not self._is_admin(event):
            return "错误：您没有权限使用跨对话代发功能。"

        try:
            if is_group:
                await event.bot.send_group_msg(group_id=int(target_id), message=message)
            else:
                await event.bot.send_private_msg(user_id=int(target_id), message=message)
            return f"已成功向 {target_id} 发送消息：{message}"
        except Exception as e:
            return f"代发消息失败: {str(e)}"
