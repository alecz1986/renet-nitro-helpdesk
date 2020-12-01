<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
  <xsl:choose>
    <xsl:when test="not(/R/data)">
    </xsl:when>
    <xsl:otherwise>
    <xsl:if test="/R/data/@auto = '1'">
      <h4>Подобрать шины</h4>
    </xsl:if>
    <form method="POST">
      <xsl:attribute name="action"><xsl:value-of select="/R/page/path_info"/></xsl:attribute>
      <xsl:for-each select='/R/form/*'>
        <xsl:if test="./ftype[text()='hidden']">
          <div>
            <xsl:element name="input">
              <xsl:attribute name="type">hidden</xsl:attribute>
              <xsl:attribute name="name"><xsl:value-of select="./name"/></xsl:attribute>
              <xsl:attribute name="value"><xsl:value-of select="./value"/></xsl:attribute>
            </xsl:element>
          </div>
        </xsl:if>
      </xsl:for-each>
      <table class='form'>
        <tbody>
          <tr>
          <xsl:for-each select='/R/form/*'>
            <xsl:if test="./ftype[text()!='hidden']">
              <td align="right"><div><xsl:value-of select="./label"/></div></td>
              <td><div>
              <xsl:choose>
                <xsl:when test="./ftype[text()='select']">
                  <xsl:element name="select">
                    <xsl:attribute name="name"><xsl:value-of select="name"/></xsl:attribute>
                    <xsl:for-each select="options/*">
                      <xsl:element name="option">
                        <xsl:attribute name="value"><xsl:value-of select="value"/></xsl:attribute>
                        <xsl:if test="../../value[1]=./value[1]"><xsl:attribute name="selected"></xsl:attribute></xsl:if>
                        <xsl:value-of select="./text()"/>
                      </xsl:element>
                    </xsl:for-each>
                  </xsl:element>
                </xsl:when>
                <xsl:when test="./ftype[text()='textarea']">
                  <xsl:element name="textarea">
                    <xsl:attribute name="name"><xsl:value-of select="./name"/></xsl:attribute>
                    <xsl:attribute name="rows">15</xsl:attribute>
                    <xsl:attribute name="cols">30</xsl:attribute>
                    <xsl:value-of select="./value"/>
                  </xsl:element>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:element name="input"><xsl:attribute name="type"><xsl:value-of select="./ftype"/></xsl:attribute><xsl:attribute name="name"><xsl:value-of select="./name"/></xsl:attribute><xsl:attribute name="value"><xsl:value-of select="./value"/></xsl:attribute></xsl:element>
                </xsl:otherwise>
              </xsl:choose>
              </div></td>
            </xsl:if>
          </xsl:for-each>
         <xsl:choose>
           <xsl:when test="/R/data/@auto = '1'">
             <td align="center"><div><input type="submit" value="Найти" class="subbutton"/></div></td>
           </xsl:when>
           <xsl:otherwise>
             <td align="center"><div><input type="submit" value="Отправить" class="subbutton"/></div></td>
           </xsl:otherwise>
         </xsl:choose>
       </tr>
       </tbody>

      </table>
    </form>
   </xsl:otherwise>
  </xsl:choose>
  </xsl:template>
</xsl:stylesheet>
