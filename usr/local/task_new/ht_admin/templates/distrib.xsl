<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table class='tsimple' width='100%'>
      <xsl:for-each select='/R/data/distributor'>
        <tr>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./distrib?distrib_id=<xsl:value-of select='@distrib_id'/></xsl:attribute>
              <xsl:value-of select='@category_name'/>
            </xsl:element>
          </td>
          <td><xsl:value-of select='@discription'/></td>
          <td><xsl:value-of select='@rate'/>%</td>
          <td>
            <xsl:element name='a'>
              <xsl:attribute name='href'>./distrib?action=delete&#38;distrib_id=<xsl:value-of select='@distrib_id'/></xsl:attribute>
              удалить
            </xsl:element>
          </td>
        </tr>
      </xsl:for-each>
    </table>
    <br/><br/>
    <a href='./distrib?distrib_id=0'>Добавить запись</a>
    <br/>
  </xsl:template>
</xsl:stylesheet>

