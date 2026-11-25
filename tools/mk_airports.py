import csv,json,sys
src,dst=sys.argv[1],sys.argv[2]
out=[]
with open(src,newline='',encoding='utf-8') as f:
    for r in csv.DictReader(f):
        t=r['type']; icao=(r['icao_code'] or r['gps_code'] or '').strip(); iata=(r['iata_code'] or '').strip()
        if t in('closed','heliport','balloonport','seaplane_base'):continue
        keep = t in('large_airport','medium_airport') or (t=='small_airport' and (iata or (r['iso_country'] in('US','CA','MX') and icao and len(icao)==4)))
        if not keep or not (icao or iata):continue
        city=(r['municipality'] or r['name']).strip()
        out.append([icao,iata,round(float(r['latitude_deg']),4),round(float(r['longitude_deg']),4),city])
json.dump(out,open(dst,'w'),separators=(',',':'),ensure_ascii=False)
print(len(out))
