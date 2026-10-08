# T3 manual annotation/provenance ledger, before classification

Original BOTH identities verified before ALL parsing. Frozen executable 2a9a644.
Two safe element inventories completed. NO endpoint classification here.

Path notation in this ledger: same-expanded-name sibling ordinal (1based) in [],
see inventory path_segments for full all-child ordinals and document preorders.
All tags here unnamespaced, all observed attributes empty. Strings literal, not
pixel-coordinate/physical numeric calibration. XML text/tails retained in inventory;
comments/PIs/prefix spelling raw-only, not complete XML token inventory.

| Binding requested | Literal XML evidence | Unresolved/excluded claim |
|---|---|---|
| Document format | Both /data[1]/metadata[1]: data_id=sa_dataset, version_major=2, description=Anotacny nastroj v1.4.1; parent/xml_sid empty | Annotation-tool label not annotation quality/process audit; empty parent not independent acquisition |
| Image records/order | /data/images/image has 150 slits, 300 ushape element occurrences; src children each one. Slits first 1-50\image1.png, last 101-150\image150.png. Ushape first 1-50\video2359_0001.tiff, last 251-300\video2359_0300.tiff | XML document ordinal/source-filename sequence not acquired frame time/order guarantee. Images/videos NOT admitted or opened; no file binding or pixel verification |
| Bounding-box fields | /data/images/image[1]/boundingboxes/boundingbox[1] slits x_left_top=126,y_left_top=53,width=44,height=38; ushape 1069,87,25,26. Total boundingbox elements 5730/15137, each has x_left_top/y_left_top/width/height | Labels suggest layout, but no explicit unit/axis-origin/index convention/image dimensions/calibration fields. No visual/spatial correctness claim; these are strings, not validated measurements |
| Class/track fields | Each boundingbox/class_name/project_id=bunka. class_name/track_id present 5730/15137 times; first slits=6, ushape=0. Distinct literal ID strings 268/84 within each file | Literal repeated labels, not independent objects/trials or physical continuity/correct identity. No ID numeric coercion or cross-file reconciliation |
| Gaps/absence/occlusion/exclusion | Complete element-name vocabulary: data,metadata,data_id,parent,version_major,xml_sid,description,images,image,src,boundingboxes,boundingbox,x_left_top,y_left_top,width,height,class_name,project_id,track_id | No literal gap/occlusion/confidence/dropout/missingness/exclusion flag or causal definition in selected XML. No gap analysis, no absence=missed detection/sensor dropout. Prior article annotation-absence claim not frame-specific truth |
| Timing/scale | Same exhaustive field vocabulary, no timestamp/fps/scale/unit fields | No frame-time or physical-scale calibration. Prior article contradiction 400μm/1280px vs 1px=3.2μm EXCLUDED, not repaired/imported. No velocity conversion |
| Annotation provenance | metadata description tool label above | No literal annotator identity, reliability/inter-rater agreement, per-frame completeness or external certification bindings in XML; prior paper claims not independent validation |
| Trial/split independence | Two selected paths; metadata data_id same sa_dataset in both, parent empty | No independent trial/split/subject/acquisition replicate binding in these fields. IDs/frame counts not independence |
| Flow/endpoint/rights | No selected XML fields for fluid flow, microrobot control, treatment/physiology/rights | CFD archives excluded, not measured flow. Images/video/other docs excluded not unavailable. CC0 page assertion not component/patent/clinical clearance |

All field-name inventory examined; missing bindings mean not literal fields in THESE
XMLs, not absent elsewhere. No schema, gap recovery, tracker/detector scoring,
physical conversion, simulation or invention performance. Element/ID counts are
literal file-format inventory counts, not measured trials/cells/physics endpoints.
Annotation-ground-truth validity, bbox correctness, frame-time calibration, causal
sensor dropout and trial independence remain unverified here. STOP before endpoint
classification or separately frozen benchmark proposal.
