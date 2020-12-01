<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <div css:display='none' id='perf'><xsl:value-of select="/R/data/@perf"/></div>
    <table width="800px" class='task' cellpadding="0" cellspacing="0">
      <xsl:element name="tr">
        <xsl:attribute name="bgcolor"><xsl:value-of select="/R/page/main/bgcolor"/></xsl:attribute>
        <td><b>Отчеты </b></td>
      </xsl:element>
      <xsl:for-each select="/R/data/report">
        <tr>
          <td>
            <xsl:element name="a">
              <xsl:attribute name="href"><xsl:value-of select="/R/page/main/@link"/>/<xsl:value-of select="@link"/></xsl:attribute>
              <xsl:value-of select="@name"/>
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <br/>
  </xsl:template>
</xsl:stylesheet>
