<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <div>
      У Вас <xsl:value-of select='/R/user/sign/@bonus'/> бонусов.<br/>
      Вы можете оплатить часть или всю сумму заказа имеющимися у Вас бонусами.
    </div>
  </xsl:template>
</xsl:stylesheet>
