<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table width="90%" class='task' cellpadding="0" cellspacing="0">
      <xsl:element name="tr">
        <xsl:attribute name="bgcolor"><xsl:value-of select="/R/page/main/bgcolor"/></xsl:attribute>
        <td colspan='7' align="center"><b>Задания, назначенные Вам</b></td>
      </xsl:element>
      <tr>
        <td colspan="2">номер</td>
        <td>задание</td>
        <td>статус</td>
        <td>дата</td>
        <td>важность</td>
        <td>заказчик</td>
      </tr>
      <xsl:for-each select="/R/data/perf/th">
        <tr>
          <td>
            <xsl:element name="a">
              <xsl:attribute name="href">/glob?id=<xsl:value-of select="@id_global"/></xsl:attribute>
              <xsl:value-of select="@id_global"/>
            </xsl:element>
          </td>
          <xsl:element name="td">
            <xsl:attribute name="bgcolor"><xsl:value-of select="@css"/></xsl:attribute>
            <xsl:value-of select="@info"/>
          </xsl:element>
          <td>
            <xsl:element name="a">
              <xsl:attribute name="href">/thread?id=<xsl:value-of select="@id"/></xsl:attribute>
              <xsl:attribute name="css:color"><xsl:value-of select="@color"/></xsl:attribute>
              <xsl:value-of select="@name"/>
            </xsl:element>
          </td>
          <td><xsl:value-of select="@status"/></td>
          <td><xsl:value-of select="@creation_date"/>/<xsl:value-of select="@creation_time"/></td>
          <td><xsl:value-of select="@importance"/></td>
          <td><xsl:value-of select="@fio"/></td>
        </tr>
      </xsl:for-each>
      <tr height="20px"><td colspan='7'></td></tr>
      <xsl:element name="tr">
        <xsl:attribute name="bgcolor"><xsl:value-of select="/R/page/main/bgcolor"/></xsl:attribute>
        <td colspan='7' align="center"><b>Задания, назначенные Вами</b></td>
      </xsl:element>
      <tr>
        <td colspan="2">номер</td>
        <td>задание</td>
        <td>статус</td>
        <td>дата</td>
        <td>важность</td>
        <td>заказчик</td>
      </tr>
      <xsl:for-each select="/R/data/cust/th">
        <tr>
          <td>
            <xsl:element name="a">
              <xsl:attribute name="href">/glob?id=<xsl:value-of select="@id_global"/></xsl:attribute>
              <xsl:value-of select="@id_global"/>
            </xsl:element>
          </td>
          <xsl:element name="td">
            <xsl:value-of select="@info"/>
          </xsl:element>
          <td>
            <xsl:element name="a">
              <xsl:attribute name="href">/thread?id=<xsl:value-of select="@id"/></xsl:attribute>
              <xsl:attribute name="css:color"><xsl:value-of select="@color"/></xsl:attribute>
              <xsl:value-of select="@name"/>
            </xsl:element>
          </td>
          <td><xsl:value-of select="@status"/></td>
          <td><xsl:value-of select="@creation_date"/>/<xsl:value-of select="@creation_time"/></td>
          <td><xsl:value-of select="@importance"/></td>
          <td><xsl:value-of select="@fio"/></td>
        </tr>
      </xsl:for-each>
    </table>
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
            <xsl:attribute name="href">?limit=<xsl:value-of select="@limit"/>&amp;offset=<xsl:value-of select="@offset"/>&amp;status=<xsl:value-of select="/R/data/@status"/>&amp;title=<xsl:value-of select="/R/data/@title"/>&amp;date=<xsl:value-of select="/R/data/@date"/>&amp;user_id=<xsl:value-of select="/R/data/@user_id"/></xsl:attribute>
            <xsl:value-of select='@val'/>
          </xsl:element>  
          <xsl:text>&#160;  &#160;</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
    <xsl:value-of select='/R/data/pages/next/@val'/>
  </xsl:template>
</xsl:stylesheet>
