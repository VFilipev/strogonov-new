export function transformLodgeForSection(lodge) {
  let photoGallery = [];
  if (lodge.images?.length) {
    photoGallery = lodge.images.map((img, index) => ({
      img: img.image_webp_url || img.image_url || img.image_variants?.main || img.image_variants?.card,
      viewerImg:
        img.image_url || img.image_webp_url || img.image_variants?.main || img.image_variants?.card,
      name: img.alt_text || `Фото ${index + 1}`,
    }));
  }

  const mainImage = photoGallery.length > 0 ? photoGallery[0].img : "";
  const mainViewerImage = photoGallery.length > 0 ? photoGallery[0].viewerImg : "";

  return {
    id: lodge.id,
    name: lodge.name,
    slug: lodge.slug,
    img: mainImage,
    viewerImg: mainViewerImage,
    description: lodge.short_description || lodge.description || "",
    conveniences: lodge.conveniences || "",
    include: lodge.include || "",
    photo_gallery_set: photoGallery.length > 1 ? photoGallery.slice(1) : [],
    price_set: lodge.price_set || [],
    special_price_set: lodge.special_price_set || [],
    availability_set: lodge.availability_set || [],
    bronirui_online_url: lodge.bronirui_online_url || "",
  };
}

export function findLodgeTypeByKind(types, kind) {
  if (!types?.length) return null;
  if (kind === "cottages") {
    return types.find(
      (type) =>
        type.slug === "kottedzhi" ||
        type.name.toLowerCase().includes("коттедж") ||
        type.name.toLowerCase().includes("деревянн"),
    );
  }
  if (kind === "modular") {
    return types.find(
      (type) => type.slug === "modulnye-doma" || type.name.toLowerCase().includes("модульн"),
    );
  }
  return null;
}
