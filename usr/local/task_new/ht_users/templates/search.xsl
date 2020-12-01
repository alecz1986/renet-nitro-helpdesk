<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
 <xsl:template match="/">
  <div css:display='none' id='perf'><xsl:value-of select="/R/data/@perf"/></div>
   <xsl:if test="/R/data/th">
    <table width="800px" class='task' cellpadding="0" cellspacing="0">
      <xsl:element name="tr">
        <xsl:attribute name="bgcolor"><xsl:value-of select="/R/page/main/bgcolor"/></xsl:attribute>
        <td colspan='7' align="center"><b> </b></td>
      </xsl:element>
      <tr>
        <td>номер</td>
        <td>задание</td>
        <td>статус</td>
        <td>дата</td>
        <td>важность</td>
        <td>заказчик</td>
        <td>исполнитель</td>
      </tr>
      <xsl:for-each select="/R/data/th">
        <tr>
          <td>
            <xsl:element name="a">
              <xsl:attribute name="href"><xsl:value-of select="/R/page/main/@link"/>/glob?id=<xsl:value-of select="@id_global"/></xsl:attribute>
              <xsl:value-of select="@id_global"/>
            </xsl:element>
          </td>
          <td>
            <xsl:element name="a">
              <xsl:attribute name="href"><xsl:value-of select="/R/page/main/@link"/>/thread?id=<xsl:value-of select="@id"/></xsl:attribute>
              <xsl:value-of select="@name"/>
            </xsl:element>
          </td>
          <td><xsl:value-of select="@status"/></td>
          <td><xsl:value-of select="@date"/>/<xsl:value-of select="@time"/></td>
          <td><xsl:value-of select="@importance"/></td>
          <td><xsl:value-of select="@fio_cust"/></td>
          <td><xsl:value-of select="@fio_perf"/></td>
        </tr>
        <tr>
          <td colspan='7' align="left">
            <pre>
              <xsl:value-of select="./message"/>
            </pre>
          </td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:if>
  <br/>
  <xsl:value-of select='/R/data/pages/prev/@val'/>
  <xsl:for-each select="/R/data/pages/page">
    <xsl:choose>
      <xsl:when test='@action = "1"'>
        <b css:color='#C50069'><xsl:value-of select='@val'/></b>
        <xsl:text>&#160;  &#160;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:element name="a">
          <xsl:attribute name="href">?offset=<xsl:value-of select="@offset"/>&amp;message=<xsl:value-of select="/R/data/@message"/>&amp;title=<xsl:value-of select="/R/data/@title"/>&amp;date=<xsl:value-of select="/R/data/@date"/>&amp;field=<xsl:value-of select="/R/data/@field"/></xsl:attribute>
          <xsl:value-of select='@val'/>
        </xsl:element>  
        <xsl:text>&#160;  &#160;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:for-each>
  <xsl:value-of select='/R/data/pages/next/@val'/>
 </xsl:template>
</xsl:stylesheet>
