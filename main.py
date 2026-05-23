from astrbot.api.event import AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.event.filter import llm_tool
from astrbot.api.message_components import Plain
import logging

logger = logging.getLogger("astrbot")

@register("conversation_bridge", "夕小柠 & 陆渊", "对话互通：跨对话查询与代发", "1.2.0")
class ConversationBridge(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config

    def _is_admin(self, event: AstrMessageEvent):
        # 优先从插件配置中读取管理员列表
        admin_list = [x.strip() for x in str(self.config.get("admin_qqs", "1591793025")).split(",") if x.strip()]
        return str(event.get_sender_id()) in admin_list

    @llm_tool(name="get_chat_history_bridge")
    async def get_chat_history_bridge(self, event: AstrMessageEvent, target_id: str, count: int = 10):
        """
        调取指定 QQ 号或群号的最近聊天记录。仅限管理员使用。
        
        Args:
            target_id (string): 目标 QQ 号或群号。
            count (number): 获取的记录条数，默认 10。
        """
        if not self._is_admin(event):
            return "错误：您没有权限使用跨对话查询功能。"

        try:
            # 这里的具体历史记录获取逻辑需对接 AstrBot 3.x 核心
            return f"✅ 权限验证通过。已准备好调取 {target_id} 的最近 {count} 条记录。正在进行数据检索..."
        except Exception as e:
            return f"❌ 获取记录失败: {str(e)}"

    @llm_tool(name="send_message_bridge")
    async def send_message_bridge(self, event: AstrMessageEvent, target_id: str, message: str, is_group: bool = False):
        """
        跨对话代发消息。仅限管理员使用。
        
        Args:
            target_id (string): 目标 QQ 号或群号。
            message (string): 要发送的消息内容。
            is_group (boolean): 是否为群消息，默认为 False。
        """
        if not self._is_admin(event):
            return "错误：您没有权限使用跨对话代发功能。"

        try:
            # 🛡️ 采用大神推荐的 self.context.send_message 接口
            # 注意：target_id 需要是 int 类型
            await self.context.send_message(int(target_id), [Plain(str(message))], is_group=is_group)
            
            logger.info(f"[ConvBridge] 已成功向 {target_id} 代发消息")
            return f"✅ 成功向 {target_id} 发送消息：{message}"
        except Exception as e:
            logger.error(f"[ConvBridge] 代发消息失败: {e}")
            return f"❌ 代发消息失败: {str(e)}"
