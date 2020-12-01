<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <div css:display='none' id='perf'><xsl:value-of select="/R/data/@perf"/></div>
    <table width="800px" class='task' cellpadding="0" cellspacing="0">
      <xsl:element name="tr">
        <xsl:attribute name="bgcolor"><xsl:value-of select="/R/page/main/bgcolor"/></xsl:attribute>
        <td colspan='7' align="center"><b>Задания, назначенные Вами</b></td>
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
              <xsl:text>_</xsl:text>
              <xsl:value-of select="@id_local"/>
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
        <tr height="20px"><td colspan='7'>
          <xsl:element name="a">
            <xsl:attribute name="href">/close?id=<xsl:value-of select="@id_global"/>&amp;path=<xsl:value-of select="/R/page/path"/></xsl:attribute>
            закрыть задание
          </xsl:element>
        </td></tr>
        <tr>
          <td colspan='7' align="left">
            <pre>
              <xsl:value-of select="./message"/>
            </pre>
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <br/>
  </xsl:template>
</xsl:stylesheet>
