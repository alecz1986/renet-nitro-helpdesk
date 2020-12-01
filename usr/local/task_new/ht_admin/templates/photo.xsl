<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <div>В списке категорий и при описании продукта будет показываться фотография с наибольшим весом. Для изменения главной фотографии продукта, увеличьте вес.</div>
    <a href='/private/product/import'>Вернуться к списку товаров</a><br/>
    <p class="photo">
      <xsl:for-each select='/R/data/photo'>
        <xsl:element name='img'>
          <xsl:attribute name='src'>/<xsl:value-of select="@path"/>/<xsl:value-of select="@id"/>_small.png</xsl:attribute>
          <xsl:attribute name='width'><xsl:value-of select="@x"/></xsl:attribute>
          <xsl:attribute name='height'><xsl:value-of select="@y"/></xsl:attribute>
          <xsl:attribute name='border'>0</xsl:attribute>
        </xsl:element>
       <em>
       <xsl:element name='a'>
          <xsl:attribute name='href'>/private/product/photo?action=check&#38;photo_id=<xsl:value-of select="@id"/>&#38;weight=-100&#38;product_id=<xsl:value-of select="@prod_id"/></xsl:attribute>
          -
        </xsl:element>
        Вес: <xsl:value-of select="@weight"/>
        <xsl:element name='a'>
          <xsl:attribute name='href'>/private/product/photo?action=check&#38;photo_id=<xsl:value-of select="@id"/>&#38;weight=100&#38;product_id=<xsl:value-of select="@prod_id"/></xsl:attribute>
         + 
       </xsl:element>
       <xsl:element name='a'>
         <xsl:attribute name='href'>/private/product/photo?action=delete&#38;photo_id=<xsl:value-of select="@id"/>&#38;product_id=<xsl:value-of select="@prod_id"/></xsl:attribute>
         <xsl:attribute name='class'>del</xsl:attribute>
         удалить фото 
       </xsl:element>
     </em>
     </xsl:for-each>
   </p>
   <br/>
   <br/>
  </xsl:template>
</xsl:stylesheet>
