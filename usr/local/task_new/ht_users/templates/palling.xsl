<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <h4><xsl:value-of select="/R/data/@vote_title"/></h4>
    <xsl:element name="form">
      <xsl:attribute name="action"><xsl:value-of select="/R/page/path_info"/></xsl:attribute>
      <xsl:attribute name="method">post</xsl:attribute>
      <div>
        <xsl:element name="input">
          <xsl:attribute name="type">hidden</xsl:attribute>
          <xsl:attribute name="name">vote</xsl:attribute>
          <xsl:attribute name="value"><xsl:value-of select="/R/data/@vote"/></xsl:attribute>
        </xsl:element>
      </div>
      <div>
        <xsl:element name="input">
          <xsl:attribute name="type">hidden</xsl:attribute>
          <xsl:attribute name="name">action</xsl:attribute>
          <xsl:attribute name="value"><xsl:value-of select="/R/data/@action"/></xsl:attribute>
        </xsl:element>
      </div>
      <div>
        <xsl:element name="input">
          <xsl:attribute name="type">hidden</xsl:attribute>
          <xsl:attribute name="name">order</xsl:attribute>
          <xsl:attribute name="value"><xsl:value-of select="/R/data/@order"/></xsl:attribute>
        </xsl:element>
      </div>
      <table border='0'>
        <tbody>
          <xsl:for-each select="/R/data/qs/q">
           <tr>
             <td>
              <xsl:element name="input">
                <xsl:attribute name="type">radio</xsl:attribute>
                <xsl:attribute name="id">rad<xsl:value-of select="@value"/></xsl:attribute>
                <xsl:attribute name="name">voice</xsl:attribute>
                <xsl:attribute name="value"><xsl:value-of select="@value"/></xsl:attribute>
              </xsl:element>
             </td>
             <th align='left'>
              <xsl:element name="label">
                <xsl:attribute name="for">rad<xsl:value-of select="@value"/></xsl:attribute>
                <xsl:value-of select="@text"/>
              </xsl:element>
             </th>
           </tr>
          </xsl:for-each>
          <tr><td colspan="2"><div><input type="submit" value="Отправить"/></div></td></tr>
        </tbody>
      </table>
    </xsl:element>
  </xsl:template>
</xsl:stylesheet>
