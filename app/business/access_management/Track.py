# export
#
#
# class AccessCodeService {
#
# private baseUrl = environment.baseUrlRestServices;
#
# constructor(private http: HttpClient
#
# ) {}
#
# getCurrentCode(): current > {
# return this.http.post < AccessCode > (this.baseUrl + 'accesscodemanagement/v1/accesscode/current', {});
# }
#
# callNextCode(): Observable < NextCodeCto > {
# return this.http.post < NextCodeCto > (this.baseUrl + 'accesscodemanagement/v1/accesscode/next', {});
# }
#
# getCodeByUuid(uuid: {'uuid': string}): Observable < AccessCode > {
# return this.http.post < AccessCode > (this.baseUrl + 'accesscodemanagement/v1/accesscode/uuid', uuid);
# }
#
# getEstimatedTimeByCode(code: AccessCode): Observable < EstimatedTime > {
# return this.http.post < EstimatedTime > (this.baseUrl + 'accesscodemanagement/v1/accesscode/estimated', code);
# }
#
# getRemainingCodesCount(): Observable < RemainingCodes > {
# return this.http.post < RemainingCodes > (this.baseUrl + 'accesscodemanagement/v1/accesscode/remaining', {});
# }
# }
#
# export
#
#
# class QueueService {
#
# private baseUrl = environment.baseUrlRestServices;
#
# constructor(private http: HttpClient
#
# ) {}
#
# getTodaysQueue(): Observable < Queue > {
# return this.http.get < Queue > (this.baseUrl + 'queuemanagement/v1/queue/daily/');
# }
#
# startQueue(queue: Queue): Observable < Queue > {
# return this.http.post < Queue > (this.baseUrl + 'queuemanagement/v1/queue/start', queue);
# }
# }