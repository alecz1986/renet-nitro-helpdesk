<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <h4>Вход с паролем</h4>
    <xsl:element name="form">
      <xsl:attribute name="action"><xsl:value-of select="/R/page/path_info"/></xsl:attribute>
      <xsl:attribute name="method">post</xsl:attribute>
      <div>
        <xsl:element name="input">
          <xsl:attribute name="type">hidden</xsl:attribute>
          <xsl:attribute name="name">auth_tries</xsl:attribute>
          <xsl:attribute name="value"><xsl:value-of select="/R/form/auth_tries/value"/></xsl:attribute>
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
      <table class="form">
        <tbody>
          <tr>
            <th align='right'><div>Логин</div></th>
            <td>
              <xsl:element name="input">
                <xsl:attribute name="type">text</xsl:attribute>
                <xsl:attribute name="name">auth_name</xsl:attribute>
                <xsl:attribute name="value"><xsl:value-of select="/R/data/auth_name/value"/></xsl:attribute>
              </xsl:element>
            </td>
          </tr>
          <tr><th align='right'><div>Пароль</div></th><td><input type="password" name="auth_key"/></td></tr>
          <tr><td colspan="2"><div><input class="subbutton" type="submit" value="Войти"/></div></td></tr>
        </tbody>
      </table>
      <table class="thead" id="page_tail">
        <tr><td><a href='/forgot'>Забыли пароль</a><a href='/register'>Зарегистрироваться</a></td></tr>
      </table>
    </xsl:element>
    <br/>
  </xsl:template>
</xsl:stylesheet>
