/**
 * \file drm_memory.c
 * Memory management wrappers for DRM
 *
 * \author Rickard E. (Rik) Faith <faith@valinux.com>
 * \author Gareth Hughes <gareth@valinux.com>
 */

/*
 * Created: Thu Feb  4 14:00:34 1999 by faith@valinux.com
 *
 * Copyright 1999 Precision Insight, Inc., Cedar Park, Texas.
 * Copyright 2000 VA Linux Systems, Inc., Sunnyvale, California.
 * All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice (including the next
 * paragraph) shall be included in all copies or substantial portions of the
 * Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * VA LINUX SYSTEMS AND/OR ITS SUPPLIERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
 * OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

#include <linux/highmem.h>
#include "drmP.h"

#ifdef DEBUG_MEMORY
#include "drm_memory_debug.h"
#else

/** No-op. */
void drm_mem_init(void)
{
}

/**
 * Called when "/proc/dri/%dev%/mem" is read.
 *
 * \param buf output buffer.
 * \param start start of output data.
 * \param offset requested start offset.
 * \param len requested number of bytes.
 * \param eof whether there is no more data to return.
 * \param data private data.
 * \return number of written bytes.
 *
 * No-op.
 */
int drm_mem_info(char *buf, char **start, off_t offset,
		 int len, int *eof, void *data)
{
	return 0;
}

/** Wrapper around kmalloc() and kfree() */
void *drm_realloc(void *oldpt, size_t oldsize, size_t size, int area)
{
	void *pt;

	if (!(pt = kmalloc(size, GFP_KERNEL)))
		return NULL;
	if (oldpt && oldsize) {
		memcpy(pt, oldpt, oldsize);
		kfree(oldpt);
	}
	return pt;
}

#if __OS_HAS_AGP
static void *agp_remap(unsigned long offset, unsigned long size,
		       struct drm_device * dev)
{
	unsigned long *phys_addr_map, i, num_pages =
	    PAGE_ALIGN(size) / PAGE_SIZE;
	struct drm_agp_mem *agpmem;
	struct page **page_map;
	void *addr;

	size = PAGE_ALIGN(size);

#ifdef __alpha__
	offset -= dev->hose->mem_space->start;
#endif

	list_for_each_entry(agpmem, &dev->agp->memory, head)
		if (agpmem->bound <= offset
		    && (agpmem->bound + (agpmem->pages << PAGE_SHIFT)) >=
		    (offset + size))
			break;
	if (!agpmem)
		return NULL;

	/*
	 * OK, we're mapping AGP space on a chipset/platform on which memory accesses by
	 * the CPU do not get remapped by the GART.  We fix this by using the kernel's
	 * page-table instead (that's probably faster anyhow...).
	 */
	/* note: use vmalloc() because num_pages could be large... */
	page_map = vmalloc(num_pages * sizeof(struct page *));
	if (!page_map)
		return NULL;

	phys_addr_map =
	    agpmem->memory->memory + (offset - agpmem->bound) / PAGE_SIZE;
	for (i = 0; i < num_pages; ++i)
		page_map[i] = pfn_to_page(phys_addr_map[i] >> PAGE_SHIFT);
	addr = vmap(page_map, num_pages, VM_IOREMAP, PAGE_AGP);
	vfree(page_map);

	return addr;
}

/** Wrapper around agp_allocate_memory() */
DRM_AGP_MEM *drm_alloc_agp(struct drm_device * dev, int pages, u32 type)
{
	return drm_agp_allocate_memory(dev->agp->bridge, pages, type);
}

/** Wrapper around agp_free_memory() */
int drm_free_agp(DRM_AGP_MEM * handle, int pages)
{
	return drm_agp_free_memory(handle) ? 0 : -EINVAL;
}

/** Wrapper around agp_bind_memory() */
int drm_bind_agp(DRM_AGP_MEM * handle, unsigned int start)
{
	return drm_agp_bind_memory(handle, start);
}

/** Wrapper around agp_unbind_memory() */
int drm_unbind_agp(DRM_AGP_MEM * handle)
{
	return drm_agp_unbind_memory(handle);
}

#else  /*  __OS_HAS_AGP  */
static inline void *agp_remap(unsigned long offset, unsigned long size,
			      struct drm_device * dev)
{
	return NULL;
}

#endif				/* agp */

#endif				/* debug_memory */

void drm_core_ioremap(struct drm_map *map, struct drm_device *dev)
{
	if (drm_core_has_AGP(dev) &&
	    dev->agp && dev->agp->cant_use_aperture && map->type == _DRM_AGP)
		map->handle = agp_remap(map->offset, map->size, dev);
	else
		map->handle = ioremap(map->offset, map->size);
}
EXPORT_SYMBOL(drm_core_ioremap);

void drm_core_ioremap_wc(struct drm_map *map, struct drm_device *dev)
{
	map->handle = ioremap_wc(map->offset, map->size);
}
EXPORT_SYMBOL(drm_core_ioremap_wc);
void drm_core_ioremapfree(struct drm_map *map, struct drm_device *dev)
{
	if (!map->handle || !map->size)
		return;

	if (drm_core_has_AGP(dev) &&
	    dev->agp && dev->agp->cant_use_aperture && map->type == _DRM_AGP)
		vunmap(map->handle);
	else
		iounmap(map->handle);
}
EXPORT_SYMBOL(drm_core_ioremapfree);