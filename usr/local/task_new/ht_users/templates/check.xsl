<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <br/>
    <h1><xsl:value-of select='/R/page/title'/></h1>
    <div css:width="45%" css:float='left' css:margin-top="25px">
      Если Вы уже зарегистрировались на нашем сайте, введите логин и пароль.
      <br/>
      <br/>
      В противном случае, выберите <a href="/register?qwick_reg=1&#38;docart=1" css:color="#C50069"><img src="/reg.png" border="0" height="23px"/></a> или <a href="/qwick_reg" css:color="#C50069"><img src="/reg2.png" border="0" height="23px"/></a>
    </div>
    <div css:width="50%" css:float='left' css:margin-top="0px" align="right">
    <xsl:element name="form">
      <xsl:attribute name="action">/public/auth/docart</xsl:attribute>
      <xsl:attribute name="method">post</xsl:attribute>
      <div>
        <xsl:element name="input">
          <xsl:attribute name="type">hidden</xsl:attribute>
          <xsl:attribute name="name">auth_tries</xsl:attribute>
          <xsl:attribute name="value">1</xsl:attribute>
        </xsl:element>
      </div>
      <xsl:for-each select="/R/ivars/ivar">
        <div>
          <xsl:element name="input">
            <xsl:attribute name="type">hidden</xsl:attribute>
            <xsl:attribute name="name"><xsl:value-of select="./name"/></xsl:attribute>
            <xsl:attribute name="value"><xsl:value-of select="./value"/></xsl:attribute>
          </xsl:element>
        </div>
      </xsl:for-each>
      <table class="tsimple" css:border-right="0px" css:border-bottom="0px">
        <tbody>
          <tr>
            <th align='right'><div>Логин</div></th>
            <td css:border="0px">
              <xsl:element name="input">
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="name">auth_name</xsl:attribute>
                <xsl:attribute name="border">0px</xsl:attribute>
                <xsl:attribute name="value"><xsl:value-of select="/R/data/auth_name/value"/></xsl:attribute>
              </xsl:element>
            </td>
          </tr>
          <tr><th align='right'><div>Пароль</div></th><td css:border="0px"><input type="password" name="auth_key"/></td></tr>
          <tr><td css:border="0px"><div><input class="subbutton" type="submit" value="Войти"/></div></td><td css:border="0px"><a href="/forgot" css:color="#C50069">Забыли пароль?</a></td></tr>
        </tbody>
      </table>
    </xsl:element>
    </div>
  </xsl:template>
</xsl:stylesheet>
