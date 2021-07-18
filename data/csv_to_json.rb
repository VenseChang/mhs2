require 'csv'
require 'json'
require 'open-uri'

def blank?(el)
  el.nil? || el.strip == ''
end

def present?(el)
  !blank?(el)
end

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT4mHLQ1NJxj3Vyvw687ufk4UVNoIIhz-QCoDbNeLciXeb8eJ6w5NJpKoSM6FlWpM5p0mBu5Jb2-eJg/pub?gid=1350087647&single=true&output=csv'
csv = CSV.parse(open(url, encoding: 'utf-8'), headers: true)

json = {}
csv.each do |row|
  no        = row['NO'].to_i
  name_c    = row['中文名']
  name_e    = row['英文名']
  egg       = row['蛋']
  normal    = row['一般狀態']
  angry     = row['生氣狀態']
  nest      = row['歸巢加成']
  weakness  = row['弱點屬性']
  part      = row['一般（非部位時）']
  head      = row['頭部']
  body      = row['身體']
  wing      = row['翅膀']
  abdomen   = row['腹部']
  feet      = row['腳']
  tail      = row['尾巴']

  next if blank?(name_c)

  key = "(#{no}) - #{name_c}"
  json[key] = {
    no: no,
    name: {
      'zh-hant': name_c,
      'en': name_e,
    },
    egg: egg,
    normal: normal,
    parts: {}
  }

  json[key][:angry] = angry if present?(angry)
  json[key][:nest] = nest if present?(nest)
  json[key][:weakness] = weakness if present?(weakness)
  json[key][:parts][:normal] = part if present?(part)
  json[key][:parts][:head] = head if present?(head)
  json[key][:parts][:body] = body if present?(body)
  json[key][:parts][:wing] = wing if present?(wing)
  json[key][:parts][:abdomen] = abdomen if present?(abdomen)
  json[key][:parts][:feet] = feet if present?(feet)
  json[key][:parts][:tail] = tail if present?(tail)
end

file = File.open('data-staging.json', 'wb')
file.write(json.to_json)
file.close
