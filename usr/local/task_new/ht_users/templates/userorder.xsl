<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <table border='1' cellspacing ='0' cellpadding='0' class='tsimple' width='100%'>
      <tr class='top'><td>Номер заказа</td><td>Дата</td><td>Статус</td><td class='no'>Сумма заказа</td></tr>
        <xsl:for-each select="/R/data/orders/order">
          <tr>
            <td>
              <xsl:element name='a'>
                <xsl:attribute name='href'>/public/order?order_id=<xsl:value-of select='@id'/></xsl:attribute>
                <xsl:value-of select='@id'/>
              </xsl:element>
            </td>
            <td class='black'><xsl:value-of select='@date'/></td>
            <td class='black'><xsl:value-of select='@status'/></td>
            <td class='no_black'><xsl:value-of select='@amount'/></td>
          </tr>
        </xsl:for-each>
    </table>
    </xsl:template>
</xsl:stylesheet>

