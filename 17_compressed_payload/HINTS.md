# HINTS // 17 COMPRESSED PAYLOAD

## pack / unpack
<details><summary>Hint</summary>

Every one of those modules has `.compress` and `.decompress`. Make a dict mapping each name to
its module (`{"zlib": zlib, ..., "zstd": zstd}`) and look the name up.
</details>

## best_algo
<details><summary>Hint</summary>

`min(ALGOS, key=lambda a: len(pack(data, a)))`. `min` keeps the first of any ties.
</details>

## stream_pack
<details><summary>Hint</summary>

`c = zlib.compressobj()`. Join `c.compress(chunk)` for each chunk, then add `c.flush()` at the
end. Without the flush you lose the tail.
</details>

## gzip_file
<details><summary>Hint</summary>

Open both files in one `with`: `open(src, "rb") as fin, gzip.open(dst, "wb") as fout`, then
`shutil.copyfileobj(fin, fout)`.
</details>

## zip_manifest
<details><summary>Hint</summary>

`z.infolist()` gives `ZipInfo` objects with `.filename` and `.file_size`.
</details>

## build_tar
<details><summary>Hint</summary>

`tarfile.open(tar_path, "w:xz")`, then `t.add(folder, arcname=Path(folder).name)`.
</details>

## safe_extract
<details><summary>Hint</summary>

`t.extractall(dest, filter="data")`. The filter raises a `tarfile.FilterError` subclass for
anything that would escape `dest`.
</details>

## make_app
<details><summary>Hint</summary>

`zipapp.create_archive(src_dir, target, main=main)`
</details>
